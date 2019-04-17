.section .rodata
.global main
CS335_format: .string "%d\n"
main:
push %rbp
mov %rsp, %rbp
sub $24, %rsp
mov $4,%rbx
mov %rbx, -16(%rbp)
mov $33,%rcx
mov %rcx, -8(%rbp)
mov  -16(%rbp) , %rdx
mov -8(%rbp), %rsi
add %rsi, %rdx
mov %rdx, %r8
mov %r8, %rax
mov %r8, -24(%rbp) 
mov $CS335_format, %rdi
mov %rax, %rsi
mov $0, %rax
call printf
mov $0, %rax
leave
ret
