hello: .string "Hello, world!"    # zero-terminated C string
format:  .string "%d"

var: .int 12


.global main
main:
    push    %rbp
    mov     %rsp,  %rbp                 # create a stack frame

    mov $format, %rdi
    
    lea -0x10(%rbp),%rsi
    call scanf
    
    mov -0x10(%rbp),%rsi
    mov     $format, %rdi
    call    printf                        #  as the first arg for puts

    mov     $0,    %eax                 # return value = 0.  Normally xor %eax,%eax
    leave                               # tear down the stack frame
    ret
