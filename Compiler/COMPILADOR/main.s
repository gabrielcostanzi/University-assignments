.section .data
tipoNum: .asciz "%d"
tipoFloat: .asciz "%f"
tipoString: .asciz "%s"
escreva: .space 1000
I_2: .float 0.0


.section .text
.globl _start
_start:
finit
lea  escreva, %edi
movb $'0', (%edi)
inc %edi
movb $'.', (%edi)
inc %edi
movb $'0', (%edi)
inc %edi
movb $0, (%edi)
pushl $escreva
call atof
addl $4, %esp
fstl I_2
para_true_3:
lea  escreva, %edi
movb $'5', (%edi)
inc %edi
movb $'.', (%edi)
inc %edi
movb $'0', (%edi)
inc %edi
movb $0, (%edi)
pushl $escreva
call atof
addl $4, %esp
fldl I_2
subl $8, %esp
fstl (%esp)
popl %eax
popl %ebx
cmpl %ebx, %eax
jg para_false_3
pushl %eax
pushl %ebx
pushl %ecx
pushl %edx
fldl I_2
subl $8, %esp
fstl (%esp)
lea escreva, %edi
movb $'%', (%edi)
inc %edi
movb $'f', (%edi)
inc %edi
movb $0, (%edi)
pushl $escreva
call printf
addl $8, %esp
popl %edx
popl %ecx
popl %ebx
popl %eax
lea  escreva, %edi
movb $'1', (%edi)
inc %edi
movb $'.', (%edi)
inc %edi
movb $'0', (%edi)
inc %edi
movb $0, (%edi)
pushl $escreva
call atof
addl $4, %esp
fldl I_2
subl $8, %esp
fstl (%esp)
fadd %st(1), %st(0)
fstl I_2
jmp para_true_3
para_false_3:
pushl $0
call exit
