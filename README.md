# Mysql-Flask-Login

Flask - MySQL - Login
Bu login kısmında yaptığım şey flash mesajı sağlamak , ve username password kayıt olan kullanıcı MySQL tablosundaki bilgileri göre giriş yapmasını sağladım. 
Mesela kullanıcı ve password MySQL tablosunda var ise ona göre olumlu yok ise olumsuz , Password sha256 methodu kullanarak şifreli bir parola sağladım.
Kullanıcının tüm bilgilerini alması için fetchone() kullandım. 
Şifreli olduğu için verify methodu kullanarak bu şifreleri doğrulamasını istedim ona göre giriş yapmasını sağladım.
