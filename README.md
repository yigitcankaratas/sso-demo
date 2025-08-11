Keycloak Kurulumu:
- İlk olarak imajı çekmek için "docker pull quay.io/keycloak/keycloak:26.0.5" komutunu terminalde çalıştırıyoruz
- Daha sonra "docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:26.0.5 start-dev" komutu ile geliştirme modunda çalıştırıyoruz.

Keycloak ile realm ve client oluşturma:
- Kurulumu yaptıktan sonra localhost:8080 ile keycloak a giriyoruz
- kullanıcı adı admin, şifre admin olacak şekilde giriş yapıyoruz
- sol üstte bulunan kısımdan myrealm adında yeni bir realm oluşturuyoruz.
- users kısmından yeni bir kullanıcı ekliyoruz
- client kısmında create clienta tıklıyoruz ve client type = saml, clientid = http://localhost:5000/metadata/ yapıp nexte basıyoruz.
- sonraki pencerede Valid redirect URIs ve Master SAML Processing URL kısımlarını http://localhost:5000/acs yapıyoruz ve kaydediyoruz.
- oluşturulan clientı açıyoruz ve Keys sekmesinde bulunan Signing keys config ve Encryption keys config alanlarını kapatıyoruz.
- son olarak advanced sekmesindeki Assertion Consumer Service POST Binding URL kısmına yine http://localhost:5000/acs yazıyoruz.
