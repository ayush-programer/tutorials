# ARMv7

A32 is the instruction set named ARM in the ARMv7 architecture; A32 uses 32-bit fixed-length instructions.

# ARMv8

AArch64 and AArch32 are the 64-bit and 32-bit general-purpose register width states of the ARMv8 architecture. Aarch32 is broadly compatible with the ARMv7-A architecture.

## Registers

|   register   |             purpose              |
|--------------|----------------------------------|
|     `x0`     | parameter / temporary / result   |
|  `x1 - x7`   | parameter / temporary            |
|     `x8`     | indirect result location         |
|  `x9 - x15`  | scratch                          |
| `x16 - x17`  | intra-procedure-call / temporary |
|    `x18`     | platform register / temporary    |
| `x19 - x28`  | callee-saved / temporary         |
|    `x29`     | frame pointer                    |
|    `x30`     | link register                    |
|     `sp`     | stack pointer                    |
|    `xzr`     | zero register                    |

Note: Sometimes, "non-volatile" is used as synonym for "callee-saved".

Note: Frame pointer is useful for debugging; it should point at the top of the stack for the current function. The link register is the address to which the program counter will return to after current function exits.

Note: The corresponding 32-bit registers are prefixed by `w` (word) instead of `x` (extended word).

Note: More information on register and procedure conventions (AAPCS64) for AArch64 can be found [here](https://developer.arm.com/documentation/ihi0055/c/).

Note: Stack pointer must point to a 16-byte aligned address (as opposed to 8-byte in AArch32).

## A64

A64 is the instruction set available in AArch64 state.

### Arithmetic operations

|    instruction    |     formula     |
|-------------------|-----------------|
| `add Rd, Rm, Rn`  | `Rd = Rm + Rn`  |
| `sub Rd, Rm, Rn`  | `Rd = Rm - Rn`  |
| `mul Rd, Rm, Rn`  | `Rd = Rm * Rn`  |

### Logical bitwise operations

|    instruction    |     formula     |
|-------------------|-----------------|
| `and Rd, Rm, Rn`  | `Rd = Rm & Rn`  |
| `bic Rd, Rm, Rn`  | `Rd = Rm & ~Rn` |
| `orr Rd, Rm, Rn`  | `Rd = Rm \| Rn` |
| `eor Rd, Rm, Rn`  |`Rd = Rm XOR Rn` |

Note: The `bic` instruction is a "reverse mask". That is, where `Rs` is `1`, it will set the bits in `Rd` to `0`.

### Compare and Branch

Compare and branch to label if Rs is zero:

```
cbz Rs, label
```

Compare and branch to label if Rs is not zero:

```
cbnz Rs, label
```

## Exception Level

In ARMv8, there are four exception levels:

* **EL0** - application
* **EL1** - operating system
* **EL2** - hypervisor
* **EL3** - secure monitor (firmware)

### Change Exception Level

In order to change exception level, you have to:

 * select the exception level and stack pointer in `spsr_elx` system register
 * load the entry address to `elr_elx` system register
 * call `eret`

### Hypervisor

Hypervisor provides same abstraction for the operating system as operating system provides for user-space applications.

#### Type 1 (Bare-Metal) Hypervisor

Bare metal hypervisor sits directly on hardware. Xen Project is one example.

<table>
	<tbody>
		<tr>
			<td align="center">Guest App</td>
			<td align="center">Guest App</td>
			<td align="center">Guest App</td>
			<td align="center">Guest App</td>
		</tr>
		<tr>
			<td align="center" colspan=2>Guest OS</td>
			<td align="center" colspan=2>Guest OS</td>
		</tr>
		<tr>
			<td align="center" colspan=4>Hypervisor</td>
		</tr>
		<tr>
			<td align="center" colspan=4>Hardware</td>
		</tr>
	</tbody>
</table>

#### Type 2 (Hosted) Hypervisor

Hosted hypervisor runs on top of an OS (or are part of one, like KVM is part of Linux).

<table>
	<tbody>
		<tr>
			<td align="center">Guest App</td>
			<td align="center">Guest App</td>
			<td align="center" colspan=2></td>
		</tr>
		<tr>
			<td align="center" colspan=2>Guest OS</td>
			<td align="center">Host App</td>
			<td align="center">Host App</td>
		</tr>
		<tr>
			<td align="center" colspan=4>Hypervisor</td>
		</tr>
		<tr>
			<td align="center" colspan=4>Hardware</td>
		</tr>
	</tbody>
</table>

### Configuration

Hypervisor is configured via [Hypervisor Configuration Register](#Hypervisor-Configuration-Register).

## System registers

You can find an extensive list of AArch64 System Registers [here](https://developer.arm.com/docs/ddi0595/h/aarch64-system-registers). Usually, each system register can be read by using:

```
mrs Rd, <system register>
```

### Multiprocessor Affinity Register

Used to identify CPU cores and clusters. Read with:

```
mrs Rd, mpidr_el1
```

For example, to find out the core on which the code is running:

```
mrs x0, mpidr_el1
and x0, x0, 0xFF
```

Register `x0` will contain core ID.

### Current Exception Level Register

Use the following command to get the current exception level:

```
mrs Rd, CurrentEL
```

In fact, the exception level is contained in bits `3:2`, so something like this is very useful:

```
.macro curr_el_to reg
mrs \reg, CurrentEL
lsr \reg, \reg, #2
and \reg, \reg, #0xFF
.endm
```

Then, you can simply get current EL to e.g. `x0` by calling `curr_el_to x0`.

### Exception Link Register

When taking an exception to ELx, holds the address to return to. For usage, see [Change Exception Level](#Change-Exception-Level) section. Defined for EL3, EL2 and EL1.

### Saved Program Status Register

### Secure Configuration Register

Called from EL3 only. Defines the configuration of the current Security state. Most important bits are:

 * NS (0): security state of EL0 and EL1
 * IRQ (1): route IRQs to EL3
 * SMC (7): disable SMC instructions
 * HCE (8): enable HVC instructions
 * RW (10): execution state at lower ELs

Note: Except IRQs, it also configures whether exceptions and other various operations are taken or trapped to EL3.

To set, use, e.g.:

```
msr scr_el3, Rm
```

### Hypervisor Configuration Register

Can be called from EL3 and EL2. Provides configuration controls for virtualization, including defining whether various operations are trapped to EL2. The most important bits are:

 * IMO (4): physical IRQ routing
 * HCD (29): HVC instruction disable
 * RW (31): execution state at lower ELs

To set, use, e.g.:

```
msr hcr_el2, Rm
```

# Notes

The best place to find information on ARM (Acorn RISC Machines) Architecture is [here](https://developer.arm.com/documentation/).

