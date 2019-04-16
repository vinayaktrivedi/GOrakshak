.section .rodata
.global main
CS335_format: .string "%d\n"
FibonacciRecursion1:
push %rbp
mov %rsp, %rbp
sub $0, %rsp
mov  16(%rbp) , %rbx
cmp $1, %rbx
setle %al
movbzl %al, %rax
mov %rax, %rbx
mov %rbx, %rax
cmp %rax, $0
je CS335_4
mov 16, %rax
leave
ret
CS335_4:
mov  16(%rbp) , %rbx
sub $1, %rbx
push %rbx
call FibonacciRecursion1
mov %rax, %rbx
mov  16(%rbp) , %rcx
sub $2, %rcx
push %rcx
call FibonacciRecursion1
mov %rax, %rbx
push %rcx
add %rbx, %rcx
mov %rcx, %rax
leave
ret
foo1:
push %rbp
mov %rsp, %rbp
<<<<<<< HEAD
sub $8, %rsp
mov  16(%rbp) , %rbx
sub $1, %rbx
mov %rbx, %rcx
mov 16, %rax
mov %rcx, -8(%rbp) 
leave
ret
mov -8, %rax
=======
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
mov %r14 , -88(%rbp)
mov %r15, %r14
add %rdx, %r14
mov %r13 , -80(%rbp)
mov %r14, %r13
add %rsi, %r13
mov %r12 , -72(%rbp)
mov %r13, %r12
add %r8, %r12
mov %r11 , -64(%rbp)
mov %r12, %r11
add %r9, %r11
mov %rbx , -8(%rbp)
mov %r11, %rbx
add %r10, %rbx
mov %rcx , -16(%rbp)
mov %rbx, %rcx
push %rbx
mov -64(%rbp), %rbx
add %rbx, %rcx
mov %rbx , -64(%rbp)
mov %rcx, %rbx
push %rcx
mov -72(%rbp), %rcx
add %rcx, %rbx
mov %rcx , -72(%rbp)
mov %rbx, %rcx
push %rbx
mov -80(%rbp), %rbx
add %rbx, %rcx
mov %rbx , -80(%rbp)
mov %rcx, %rbx
push %rcx
mov -88(%rbp), %rcx
add %rcx, %rbx
mov %rcx , -88(%rbp)
mov %rbx, %rcx
push %rbx
mov -96(%rbp), %rbx
add %rbx, %rcx
mov %rbx , -96(%rbp)
mov %rcx, %rbx
push %rcx
mov -104(%rbp), %rcx
add %rcx, %rbx
mov %rcx , -104(%rbp)
mov %rbx, %rcx
mov %rcx, %rax
mov %rdx, -24(%rbp) 
mov %r8, -40(%rbp) 
mov %rsi, -32(%rbp) 
mov %r10, -56(%rbp) 
mov %r9, -48(%rbp) 
mov %rcx, -112(%rbp) 
mov $CS335_format, %rdi
mov %rax, %rsi
mov $0, %rax
call printf
mov $0, %rax
>>>>>>> e0d84456528e4b416ab855885d576d96a499baea
leave
ret
main:
push %rbp
mov %rsp, %rbp
sub $24, %rsp
push $19
call FibonacciRecursion1
mov %rax, %rbx
mov %rbx, %rcx
push $10
mov %rcx, -8(%rbp) 
call foo1
mov %rax, %rbx
mov %rax, %rcx
mov %rbx, %rdx
mov %rcx, %rsi
