; math_linux.asm - Linux x86-64 NASM Assembly Statistical Engine
; Uses the System V AMD64 Calling Convention:
; Arg1 = RDI, Arg2 = RSI, Arg3 = RDX
; Return integer = RAX, Return float = XMM0

global asm_sum
global asm_mean
global asm_variance
global asm_min
global asm_max
global asm_stddev
global asm_dot_product

section .text

; ------------------------------------------------
; int64_t asm_sum(int64_t* array (RDI), int64_t length (RSI))
; ------------------------------------------------
asm_sum:
    xor rax, rax            ; rax = 0 (sum accumulator)
    test rsi, rsi           ; check if length == 0
    jz .done
.loop:
    add rax, [rdi]          ; add element to sum
    add rdi, 8              ; move pointer 8 bytes forward (64-bit int)
    dec rsi                 ; decrement length counter
    jnz .loop               ; loop if length != 0
.done:
    ret

; ------------------------------------------------
; int64_t asm_mean(int64_t* array (RDI), int64_t length (RSI))
; ------------------------------------------------
asm_mean:
    test rsi, rsi           ; avoid division by zero
    jz .err

    push rbx                ; Save callee-saved register
    push rbp
    mov rbp, rsp

    mov rbx, rsi            ; save length in rbx before call

    ; RDI and RSI are already set up for asm_sum
    call asm_sum            ; Call our sum function

    ; rax now contains the sum. rbx contains the length.
    cqo                     ; sign extend rax into rdx:rax for division
    idiv rbx                ; rax = (rdx:rax) / rbx

    pop rbp
    pop rbx
    ret
.err:
    xor rax, rax
    ret

; ------------------------------------------------
; int64_t asm_variance(int64_t* array (RDI), int64_t length (RSI))
; ------------------------------------------------
asm_variance:
    test rsi, rsi
    jz .err

    push rbx
    push rbp
    push r12
    push r13
    mov rbp, rsp

    mov rbx, rdi            ; save array pointer in rbx
    mov r12, rsi            ; save length in r12

    call asm_mean           ; rax = mean
    mov r13, rax            ; store mean in r13

    xor rax, rax            ; rax = 0 (sum of squares accumulator)
    mov rdi, rbx            ; restore array pointer
    mov rsi, r12            ; restore length

.var_loop:
    mov r8, [rdi]           ; r8 = current element
    sub r8, r13             ; r8 = element - mean
    imul r8, r8             ; r8 = (element - mean)^2
    add rax, r8             ; sum of squares += r8

    add rdi, 8              ; next element
    dec rsi
    jnz .var_loop

    ; divide sum of squares by length to get variance
    cqo
    idiv r12                ; rax = variance

    pop r13
    pop r12
    pop rbp
    pop rbx
    ret
.err:
    xor rax, rax
    ret

; ------------------------------------------------
; int64_t asm_min(int64_t* array (RDI), int64_t length (RSI))
; ------------------------------------------------
asm_min:
    test rsi, rsi
    jz .err
    mov rax, [rdi]          ; Assume first element is min
    add rdi, 8
    dec rsi
    jz .done
.loop:
    mov r8, [rdi]           ; Load next element
    cmp r8, rax             ; Compare with current min
    jge .skip               ; If greater or equal, skip
    mov rax, r8             ; Update min
.skip:
    add rdi, 8
    dec rsi
    jnz .loop
.done:
    ret
.err:
    xor rax, rax
    ret

; ------------------------------------------------
; int64_t asm_max(int64_t* array (RDI), int64_t length (RSI))
; ------------------------------------------------
asm_max:
    test rsi, rsi
    jz .err
    mov rax, [rdi]          ; Assume first element is max
    add rdi, 8
    dec rsi
    jz .done
.loop:
    mov r8, [rdi]
    cmp r8, rax
    jle .skip               ; If less or equal, skip
    mov rax, r8             ; Update max
.skip:
    add rdi, 8
    dec rsi
    jnz .loop
.done:
    ret
.err:
    xor rax, rax
    ret

; ------------------------------------------------
; double asm_stddev(int64_t* array (RDI), int64_t length (RSI))
; ------------------------------------------------
asm_stddev:
    test rsi, rsi
    jz .err_stddev

    push rbx
    push rbp
    mov rbp, rsp

    call asm_variance       ; RAX = integer variance

    cvtsi2sd xmm0, rax      ; Convert integer in RAX to double in XMM0
    sqrtsd xmm0, xmm0       ; XMM0 = sqrt(XMM0)

    pop rbp
    pop rbx
    ret
.err_stddev:
    pxor xmm0, xmm0         ; Return 0.0 in float register
    ret

; ------------------------------------------------
; int64_t asm_dot_product(int64_t* array1 (RDI), int64_t* array2 (RSI), int64_t length (RDX))
; ------------------------------------------------
asm_dot_product:
    xor rax, rax            ; rax = 0 (accumulator)
    test rdx, rdx
    jz .done_dot
.loop_dot:
    mov r9, [rdi]           ; r9 = array1[i]
    mov r10, [rsi]          ; r10 = array2[i]
    imul r9, r10            ; r9 = array1[i] * array2[i]
    add rax, r9             ; rax += r9

    add rdi, 8              ; advance array1 pointer
    add rsi, 8              ; advance array2 pointer
    dec rdx
    jnz .loop_dot
.done_dot:
    ret
