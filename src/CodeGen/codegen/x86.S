.section .rodata
.global main
CS335_format: .string "%d\n"
main:
push %rbp
mov %rsp, %rbp
sub $112, %rsp
mov $10,%rbx
mov $10,%rcx
mov $10,%rdx
mov $10,%rsi
mov $10,%r8
mov $10,%r9
mov $10,%r10
mov $10,%r11
mov $10,%r12
mov $10,%r13
mov $10,%r14
mov $10,%r15
mov %r15 , -96(%rbp)
mov $10,%r15
mov %r15 , -104(%rbp)
mov %rbx, %r15
add %rcx, %r15
push %r15
mov %r15, %r15
add %rdx, %r15
push %r15
mov %r15, %r15
add %rsi, %r15
push %r15
mov %r15, %r15
add %r8, %r15
push %r15
mov %r15, %r15
add %r9, %r15
push %r15
mov %r15, %r15
add %r10, %r15
push %r15
mov %r15, %r15
add %r11, %r15
push %r15
mov %r15, %r15
add %r12, %r15
push %r15
mov %r15, %r15
add %r13, %r15
push %r15
mov %r15, %r15
add %r14, %r15
push %r15
mov %r15, %r15
mov %r15 , -192(%rbp)
mov -96(%rbp), %r15
add %r15, %r15
push %r15
mov %r15, %r15
mov %r15 , -200(%rbp)
mov -104(%rbp), %r15
add %r15, %r15
push %r15
mov %r15, %r15
mov %r15, %rax
mov %r14, -88(%rbp) 
mov %r13, -80(%rbp) 
mov %rbx, -8(%rbp) 
mov %rdx, -24(%rbp) 
mov %rcx, -16(%rbp) 
mov %r8, -40(%rbp) 
mov %rsi, -32(%rbp) 
mov %r10, -56(%rbp) 
mov %r9, -48(%rbp) 
mov %r12, -72(%rbp) 
mov %r11, -64(%rbp) 
mov %r15, -112(%rbp) 
mov $CS335_format, %rdi
mov %rax, %rsi
mov $0, %rax
call printf
mov $0, %rax
leave
ret
