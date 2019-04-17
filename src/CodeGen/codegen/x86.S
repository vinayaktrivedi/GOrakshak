.section .rodata
.global main
CS335_format: .string "%d\n"
main:
push %rbp
mov %rsp, %rbp
sub $200, %rsp
mov $13,%rbx
mov %rbp, %rcx
add $-8 , %rcx
mov $1 , %rdx
shl $3 , %rdx
sub %rdx , %rcx
mov $100 , %rsi
mov %rsi , (%rcx)
mov %rbp, %rcx
add $-8 , %rcx
mov $2 , %rdx
shl $3 , %rdx
sub %rdx , %rcx
mov $200 , %rsi
mov %rsi , (%rcx)
mov %rbp, %rcx
add $-8 , %rcx
mov $3 , %rdx
shl $3 , %rdx
sub %rdx , %rcx
mov $300 , %rsi
mov %rsi , (%rcx)
mov %rbp, %rcx
add $-8 , %rcx
mov $4 , %rdx
shl $3 , %rdx
sub %rdx , %rcx
mov $400 , %rsi
mov %rsi , (%rcx)
mov %rbp, %rdx
add $-8 , %rdx
mov $1 , %rsi
shl $3 , %rsi
sub %rsi , %rdx
mov (%rdx) , %rcx
mov %rbp, %r9
add $-8 , %r9
mov $2 , %r10
shl $3 , %r10
sub %r10 , %r9
mov (%r9) , %r8
add %r8, %rcx
mov %rcx, %r11
mov %rbp, %r13
add $-8 , %r13
mov $3 , %r14
shl $3 , %r14
sub %r14 , %r13
mov (%r13) , %r12
add %r12, %r11
mov %r11, %r15
mov %rbx , -192(%rbp)
push %rcx
mov %rbp, %rcx
add $-8 , %rcx
mov %rdx , -192(%rbp)
mov $4 , %rdx
shl $3 , %rdx
sub %rdx , %rcx
mov (%rcx) , %rbx
add %rbx, %r15
mov %rcx , -192(%rbp)
mov %rbp, %rcx
add $-8 , %rcx
mov %rdx , -192(%rbp)
mov $4 , %rdx
shl $3 , %rdx
sub %rdx , %rcx
mov %rbx , (%rcx)
mov %r15, %rbx
mov %rbx, %rax
mov %rbx, -184(%rbp) 
mov $CS335_format, %rdi
mov %rax, %rsi
mov $0, %rax
call printf
mov $0, %rax
leave
ret
