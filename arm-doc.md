# ARM Architecture


## ARMv7

A32 is the instruction set named ARM in the ARMv7 architecture; A32 uses 32-bit fixed-length instructions.

## ARMv8

AArch64 and AArch32 are the 64-bit and 32-bit general-purpose register width states of the ARMv8 architecture. Aarch32 is broadly compatible with the ARMv7-A architecture.

### Registers

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

### A64

A64 is the instruction set available in AArch64 state.

#### Add

```
ADD Rd, Rm, Rn <=> Rd = Rm + Rn
```

`Rn` is flexible.

#### Multiply

```
MUL Rd, Rm, Rn <=> Rd = Rm * Rn
```

`Rn` is not flexible.

#### Bitwise `and`

```
and Rd, Rs <=> Rd = Rd & Rs
```

#### Bit Clear

```
bic Rd, Rs <=> Rd = Rd & !Rs
```

This is a "reverse mask". That is, where `Rs` is `1`, it will set the bits in `Rd` to `0`.

#### Bitwise OR

```
orr Rd, Rs <=> Rd = Rd | Rs
```

#### Bitwise XOR

```
eor Rd, Rs <=> Rd = Rd XOR Rs
```

#### Compare and Branch

Compare and Branch if Zero:

```
cbz Rs, label <=> if (Rs == 0) goto label
```

Compare and Branch if Not Zero:

```
cbnz Rs, label <=> if (Rs != 0) goto label
```

### System registers

You can find an extensive list of AArch64 System Registers [here](https://developer.arm.com/docs/ddi0595/h/aarch64-system-registers). Usually, each system register can be read by using:

```
mrs Rd, <register>
```

#### Multiprocessor Affinity Register

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

### Exception Level

In ARMv8, there are four exception levels:

* **EL0** - application
* **EL1** - operating system
* **EL2** - hypervisor
* **EL3** - secure monitor (firmware)

#### Hypervisor

Hypervisor provides same abstraction for the operating system as operating system provides for user-space applications.

###### Type 1 (Bare-Metal) Hypervisor

Bare metal hypervisor sits directly on hardware. Xenial is one example.

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

##### Type 2 (Hosted) Hypervisor

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

#### Current Exception Level Register

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

#### Change Exception Level

# Notes

The best place to find information on ARM (Acorn RISC Machines) Architecture is [here](https://developer.arm.com/documentation/).

