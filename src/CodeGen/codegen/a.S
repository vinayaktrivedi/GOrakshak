#hello: .string "Hello, world!"    # zero-terminated C string
#format:  .string "%d"

#var: .int 12


#.global main
#main:
#    push    %rbp
#    mov     %rsp,  %rbp                 # create a stack frame

#    mov $format, %rdi
    
#    lea -0x10(%rbp),%rsi
#    call scanf
    
#    mov -0x10(%rbp),%rsi
#    mov     $format, %rdi
#    call    printf                        #  as the first arg for puts

#    mov     $0,    %eax                 # return value = 0.  Normally xor %eax,%eax
#    leave                               # tear down the stack frame
#    ret


#.global main
#CS335_format: .string "%d\n"
#format:  .string "%d"
#main:
#push %rbp
#mov %rsp, %rbp
#sub $12, %rsp
#mov $10,%rbx
#mov $13,%rcx
#mov %rbx, %rdx
#add %rcx, %rdx
#mov %rdx, %rsi
#mov %rsi, %rax
#mov %rbx, -4(%rbp)
#mov %rcx, -8(%rbp)
#mov %rsi, -12(%rbp)
#mov $CS335_format, %rdi
#mov %rax, %rsi
#mov $0, %rax
#call printf
#mov $0, %rax
#leave
#ret

.section .rodata
.global main
CS335_format: .string "%d\n"
main:
push %rbp
mov %rsp, %rbp
sub $12, %rsp
mov $19,%rbx
mov $14,%rcx
mov %rbx, %rdx
add %rcx, %rdx
mov %rdx, %rsi
mov %rsi, %rax
mov %rbx, -4(%rbp)
mov %rsi, -12(%rbp)
mov %rcx, -8(%rbp)
mov $CS335_format, %rdi
mov %rax, %rsi
mov $0, %rax
call printf
mov $0, %rax
leave
ret