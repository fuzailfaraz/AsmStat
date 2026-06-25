; math.asm - Win64 NASM Assembly Statistical Engine
; This file contains the core logic executed by the Python frontend.
; It uses the Microsoft x64 Calling Convention:
; Arg1 = RCX, Arg2 = RDX
; Return = RAX

global asm_sum
global asm_mean
global asm_variance
global asm_min
global asm_max
global asm_stddev
global asm_dot_product

section .text

; ------------------------------------------------
; int64_t asm_sum(int64_t* array (RCX), int64_t length (RDX))
; ------------------------------------------------
asm_sum:
    xor rax, rax            ; rax = 0 (sum accumulator)
    test rdx, rdx           ; check if length == 0
    jz .done
.loop:
    add rax, [rcx]          ; add element to sum
    add rcx, 8              ; move pointer 8 bytes forward (64-bit int)
    dec rdx                 ; decrement length counter
    jnz .loop               ; loop if length != 0
.done:
    ret

; ------------------------------------------------
; int64_t asm_mean(int64_t* array (RCX), int64_t length (RDX))
; ------------------------------------------------
asm_mean:
    test rdx, rdx           ; avoid division by zero
    jz .err
    
    ; Win64 ABI requires shadow space when calling other functions
    push rbx                ; Save callee-saved register
    push rbp
    mov rbp, rsp
    sub rsp, 32             ; Allocate 32 bytes shadow space
    
    mov rbx, rdx            ; save length in rbx before call
    
    ; RCX and RDX are already set up for asm_sum
    call asm_sum            ; Call our sum function
    
    ; rax now contains the sum. rbx contains the length.
    cqo                     ; sign extend rax into rdx:rax for division
    idiv rbx                ; rax = (rdx:rax) / rbx
    
    add rsp, 32             ; Cleanup shadow space
    pop rbp
    pop rbx
    ret
.err:
    xor rax, rax
    ret

; ------------------------------------------------
; int64_t asm_variance(int64_t* array (RCX), int64_t length (RDX))
; ------------------------------------------------
asm_variance:
    test rdx, rdx
    jz .err
    
    push rbx
    push rbp
    push rsi
    push rdi
    mov rbp, rsp
    sub rsp, 32             ; Shadow space
    
    mov rbx, rcx            ; save array pointer in rbx
    mov rsi, rdx            ; save length in rsi
    
    call asm_mean           ; rax = mean
    mov rdi, rax            ; store mean in rdi
    
    xor rax, rax            ; rax = 0 (sum of squares accumulator)
    mov rcx, rbx            ; restore array pointer
    mov rdx, rsi            ; restore length
    
.var_loop:
    mov r8, [rcx]           ; r8 = current element
    sub r8, rdi             ; r8 = element - mean
    imul r8, r8             ; r8 = (element - mean)^2
    add rax, r8             ; sum of squares += r8
    
    add rcx, 8              ; next element
    dec rdx
    jnz .var_loop
    
    ; divide sum of squares by length to get variance
    cqo
    idiv rsi                ; rax = variance
    
    add rsp, 32
    pop rdi
    pop rsi
    pop rbp
    pop rbx
    ret
.err:
    xor rax, rax
    ret

; ------------------------------------------------
; int64_t asm_min(int64_t* array (RCX), int64_t length (RDX))
; ------------------------------------------------
asm_min:
    test rdx, rdx
    jz .err
    mov rax, [rcx]          ; Assume first element is min
    add rcx, 8
    dec rdx
    jz .done
.loop:
    mov r8, [rcx]           ; Load next element
    cmp r8, rax             ; Compare with current min
    jge .skip               ; If greater or equal, skip
    mov rax, r8             ; Update min
.skip:
    add rcx, 8
    dec rdx
    jnz .loop
.done:
    ret
.err:
    xor rax, rax
    ret

; ------------------------------------------------
; int64_t asm_max(int64_t* array (RCX), int64_t length (RDX))
; ------------------------------------------------
asm_max:
    test rdx, rdx
    jz .err
    mov rax, [rcx]          ; Assume first element is max
    add rcx, 8
    dec rdx
    jz .done
.loop:
    mov r8, [rcx]
    cmp r8, rax
    jle .skip               ; If less or equal, skip
    mov rax, r8             ; Update max
.skip:
    add rcx, 8
    dec rdx
    jnz .loop
.done:
    ret
.err:
    xor rax, rax
    ret

; ------------------------------------------------
; double asm_stddev(int64_t* array (RCX), int64_t length (RDX))
; ------------------------------------------------
asm_stddev:
    test rdx, rdx
    jz .err_stddev
    
    push rbx
    push rbp
    mov rbp, rsp
    sub rsp, 32             ; Shadow space
    
    call asm_variance       ; RAX = integer variance
    
    cvtsi2sd xmm0, rax      ; Convert integer in RAX to double in XMM0
    sqrtsd xmm0, xmm0       ; XMM0 = sqrt(XMM0)
    
    add rsp, 32
    pop rbp
    pop rbx
    ret
.err_stddev:
    pxor xmm0, xmm0         ; Return 0.0 in float register
    ret

; ------------------------------------------------
; int64_t asm_dot_product(int64_t* array1 (RCX), int64_t* array2 (RDX), int64_t length (R8))
; ------------------------------------------------
asm_dot_product:
    xor rax, rax            ; rax = 0 (accumulator)
    test r8, r8
    jz .done_dot
.loop_dot:
    mov r9, [rcx]           ; r9 = array1[i]
    mov r10, [rdx]          ; r10 = array2[i]
    imul r9, r10            ; r9 = array1[i] * array2[i]
    add rax, r9             ; rax += r9
    
    add rcx, 8              ; advance array1 pointer
    add rdx, 8              ; advance array2 pointer
    dec r8
    jnz .loop_dot
.done_dot:
    ret
