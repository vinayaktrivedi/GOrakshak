.section .rodata
.global main
CS335_format: .string "%d\n"
main:
push %rbp
mov %rsp, %rbp
sub $88, %rsp
mov $10,%rbx
mov %rbx, -8(%rbp)
mov  -32(%rbp) , %rcx
mov %rcx, %rdx
mov $12,%rsi
mov %rsi, -32(%rbp)
mov  -56(%rbp) , %r8
mov %r8, %r9
mov $11,%r10
mov %r10, -56(%rbp)
mov $0,%r11
mov  -80(%rbp) , %r12
mov %r12, %r13
mov  -8(%rbp) , %r14
mov %r14, %rax
mov %rdx, -16(%rbp) 
mov %r9, -40(%rbp) 
mov %r13, -64(%rbp) 
mov %r11, -80(%rbp) 
mov %r14, -88(%rbp) 
mov $CS335_format, %rdi
mov %rax, %rsi
mov $0, %rax
call printf
mov $0, %rax
leave
ret
