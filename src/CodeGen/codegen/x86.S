.section .rodata
.global main
CS335_format: .string "%d\n"
main:
push %rbp
mov %rsp, %rbp
sub $200, %rsp
mov  -24(%rbp) , %rbx
mov %rbx, %rcx
mov %rbp, %rdx
sub $-12 , %rdx
mov $1 , %rsi
shl $2 , %rsi
sub %rsi , %rdx
mov $100 , %r8
mov %r8 , (%rdx)
mov  -24(%rbp) , %r8
mov %r8, %r9
mov %r9, %r10
mov %r10, %rax
mov %rbx, -24(%rbp) 
mov %r8, -24(%rbp) 
mov %r10, -200(%rbp) 
mov $CS335_format, %rdi
mov %rax, %rsi
mov $0, %rax
call printf
mov $0, %rax
leave
ret
