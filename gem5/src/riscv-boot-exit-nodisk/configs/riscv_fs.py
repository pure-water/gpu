# Copyright (c) 2021 The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This example runs a simple linux boot.

Characteristics
---------------

* Runs exclusively on the RISC-V ISA with the classic caches
* Assumes that the kernel and the workload are compiled into the bootloader
* Automatically generates the DTB file
* Automatically executes `m5 exit` when booting is done
"""

import m5
from m5.objects import Root

from gem5.runtime import get_runtime_isa
from gem5.components.boards.riscv_board import RiscvBoard
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.utils.requires import requires
from gem5.resources.resource import Resource, CustomResource

import argparse

def parse_options():
    parser = argparse.ArgumentParser(
        description="Full System Linux booting without disk image")

    parser.add_argument("--bbl", default=None,
                        help="Path to the bbl binary with a Linux kernel"
                             " and a workload. Default:"
                             " gem5-resources' bbl-boot-exit-nodisk")

    parser.add_argument("--cpu-type", required=True, help="CPU Type")

    parser.add_argument("--num-cpus", type=int, required=True,
                        help="Number of CPU cores")

    return parser.parse_args()

if __name__ == "__m5_main__":

    args = parse_options()
    cpu = None
    if args.cpu_type == "atomic":
        cpu = CPUTypes.ATOMIC
    elif args.cpu_type == "timing":
        cpu = CPUTypes.TIMING
    elif args.cpu_type == "o3":
        cpu = CPUTypes.O3
    else:
        assert(False, "The CPU type must be one of: {atomic, timing, o3}")

    bbl = CustomResource(args.bbl) if args.bbl else Resource('riscv-boot-exit-nodisk')

    # Run a check to ensure the right version of gem5 is being used.
    requires(isa_required=ISA.RISCV)

    from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy \
        import (
            PrivateL1PrivateL2CacheHierarchy,
        )

    # Setup the cache hierarchy. PrivateL1PrivateL2 and NoCache have been tested.
    cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
        l1d_size="32KiB", l1i_size="32KiB", l2_size="512KiB"
    )

    # Setup the system memory.
    memory = SingleChannelDDR3_1600()

    # Setup a single core Processor.
    processor = SimpleProcessor(cpu_type=cpu, num_cores=1)

    # Setup the board.
    board = RiscvBoard(
        clk_freq="1GHz",
        processor=processor,
        memory=memory,
        cache_hierarchy=cache_hierarchy,
        use_disk_image=False
    )

    board.connect_things()

    # Set the Full System workload.
    board.set_workload(
        disk_image=None,
        bootloader=bbl,
        kernel_boot_params = "console=ttyS0"
    )

    root = Root(full_system=True, system=board)

    m5.instantiate()

    print("Beginning simulation!")
    # Note: You can access the terminal upon boot using
    # m5term (`./util/term`): `./m5term localhost <port>`. Note the `<port>`
    # value is obtained from the gem5 terminal stdout. Look out for
    # "system.platform.terminal: Listening for connections on port <port>".
    exit_event = m5.simulate()
    print(
        "Exiting @ tick {} because {}.".format(m5.curTick(), exit_event.getCause())
    )
