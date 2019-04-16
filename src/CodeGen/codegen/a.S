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


.global main
#CS335format: .string "%d\n"
format:  .string "%d"
main:
push %rbp
mov %rsp, %rbp
sub $12, %rsp
mov $10,%rbx
mov $13,%rcx
mov %rbx, %rdx
add %rcx, %rdx
mov %rdx, %rsi
mov %rsi, %rax
mov %rbx, -0x4(%rbp)
mov %rcx, -0x8(%rbp)
mov %rsi, -0xc(%rbp)
mov $format, %rdi
mov %rax, %rsi
mov $0, %rax
call printf
mov $0, %rax
leave
ret