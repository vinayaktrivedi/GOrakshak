.section .rodata             # read-only static data
.globl hello
hello:
  .string "Hello, world!"    # zero-terminated C string
.globl haha
haha:.string "hahaaa"



.text
.global main
main:
    push    %rbp
    mov     %rsp,  %rbp                 # create a stack frame

    mov     $haha, %edi                # put the address of hello into RDI
    call    puts                        #  as the first arg for puts

    mov     $0,    %eax                 # return value = 0.  Normally xor %eax,%eax
    leave                               # tear down the stack frame
    ret

