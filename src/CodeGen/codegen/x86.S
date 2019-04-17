.section .rodata
.global main
CS335_format: .string "%d\n"
main:
push %rbp
mov %rsp, %rbp
sub $200, %rsp
mov $13,%rbx
mov $1000,%rcx
mov %rbp, %rdx
add $-8 , %rdx
mov $1 , %rsi
shl $3 , %rsi
sub %rsi , %rdx
mov $100 , %r8
mov %r8 , (%rdx)
mov %rbp, %rdx
add $-8 , %rdx
mov $2 , %rsi
shl $3 , %rsi
sub %rsi , %rdx
mov $200 , %r8
mov %r8 , (%rdx)
mov %rbp, %rdx
add $-8 , %rdx
mov $3 , %rsi
shl $3 , %rsi
sub %rsi , %rdx
mov $300 , %r8
mov %r8 , (%rdx)
mov %rbp, %rdx
add $-8 , %rdx
mov $4 , %rsi
shl $3 , %rsi
sub %rsi , %rdx
mov $400 , %r8
mov %r8 , (%rdx)
mov %rbp, %rsi
add $-8 , %rsi
mov $1 , %r8
shl $3 , %r8
sub %r8 , %rsi
mov (%rsi) , %rdx
mov %rbp, %r10
add $-8 , %r10
mov $2 , %r11
shl $3 , %r11
sub %r11 , %r10
mov (%r10) , %r9
add %r9, %rdx
mov %rdx, %r12
mov %rbp, %r14
add $-8 , %r14
mov $3 , %r15
shl $3 , %r15
sub %r15 , %r14
mov (%r14) , %r13
add %r13, %r12
mov %rcx , -200(%rbp)
mov %r12, %rcx  #rcx has final answer
mov %rbx , -192(%rbp)
push %rdx
mov %rbp, %rdx
add $-8 , %rdx
mov %rsi , -192(%rbp)
mov $4 , %rsi
shl $3 , %rsi
sub %rsi , %rdx
mov (%rdx) , %rbx
add %rbx, %rcx
push %rcx
mov %rbp, %rcx
add $-8 , %rcx
mov %rdx , -192(%rbp)
mov $4 , %rdx
shl $3 , %rdx
sub %rdx , %rcx
mov %rbx , (%rcx)
mov %rcx, %rbx
mov %rcx , -192(%rbp)
mov -200(%rbp), %rcx
add %rcx, %rbx
mov %rcx , -200(%rbp)
mov %rbx, %rcx
mov %rcx, %rax
mov %rcx, -184(%rbp) 
mov $CS335_format, %rdi
mov %rax, %rsi
mov $0, %rax
call printf
mov $0, %rax
leave
ret
