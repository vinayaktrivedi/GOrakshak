section	.text
global _start
main1:
push rbp
mov rbp, rsp
push eax
push ebx
push esi
push edi
push edx
mov rbx, 0
mov rcx, 0
mov -8[ebp],rcx
mov -4[ebp],rbx
