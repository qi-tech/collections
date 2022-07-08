# Exemplos para Utilização dos Serviços QITech via integração.

A QI Tech é a primeira instituição financeira a criar um modelo exclusivo de Bank-as-a-Service (BaaS) do Brasil. Nosso objetivo é ajudar qualquer Fintech/Gestora de Crédito ou empresa a ter acesso a serviços financeiros rápidos, ágeis e seguros, da maneira que quiser. Saiba mais em https://qitech.com.br.

Essa coleção tem como objetivo exemplificar a utilizar nossa API Rest.

Obs.: Em caso de dúvidas em qualquer etapa do processo favor entre em contato com [api@qitech.com.br](mailto:api@qitech.com.br) detalhando seu problema/dúvida que te auxiliaremos.

<br>
<br>


## Informações importantes

Para utilizar nossa API em produção é necessário que se entre com contato com [onboard@qitech.com.br](mailto:onboard@qitech.com.br) para contato comercial e configuração da integração.


## Antes de começar

### 1. Crie sua conta em nosso ambiente de sandbox

Para começar:

<div>
<ul>
<li class="important">
Acesse o <a href="https://sandbox.qitech.com.br/register" target="_blank">nosso ambiente sandbox</a>
</li>
<li class="important">
Siga todos os passos para iniciar a criação da sua conta.
</li>
</ul>
</div>

![Cadastro Sandbox](https://storage.googleapis.com/qitech-website-documents/documentation/cadastro.png)

### 2. Faça a troca das chaves

Toda a troca de informações entre APIs deverá utilizar o protocolo HTTPS[¹](#1) e uma assinatura  assimétrica[²](#2). Nosso modelo de implementação da assinatura é baseado no utilizado pela Amazon[³](#3), sendo a principal diferença o uso de chaves assimétricas que adicionam uma camada de não-repúdio na comunicação.

Toda a comunicação com a QI é assinada, tanto as requisições quanto as respostas, isso significa que existe um parâmetro nas mensagens que garante sua autenticidade. Para realizar tal assinatura, a QI usa um padrão com chaves assimétricas, portanto existem duas chaves diferentes, uma para assinatura (chave privada) e uma para leitura (chave pública). As assinaturas seguem o padrão JWT[⁴](#4) e o algoritmo de criptografia ECDSASHA512[⁵](#5) (Recomendamos **FORTEMENTE** a exploração do site https://jwt.io/, nele você conseguirá validar JWTs e descobrir bibliotecas para lidar com esses tokens em basicamente qualquer linguagem moderna de programação).

O uso dessa combinação de tecnologias visa criar um canal de comunicação seguro e que garanta que as mensagens enviadas só poderiam vir de uma fonte que possui a chave privada para assiná-la. Por esse motivo o par de chaves pública-privada precisa ser criado de maneira independente por cada uma das partes e a chave privada deve ser guardada em segredo, não sendo divulgada para nenhum terceiro ou parte interessada, nem mesmo a QI.

### 2.1 Gerando suas chaves pública e privada

Para gerar uma chave pública em um computador UNIX faça:

```bash
$ ssh-keygen -t ecdsa -b 521 -m PEM -f jwtECDSASHA512.key
```

<br>

E a partir desta chave privada gere sua chave pública.

```bash
$ openssl ec -in jwtECDSASHA512.key -pubout -outform PEM -out jwtECDSASHA512.key.pub
```

<br>

### 2.2 Gerando a chave pública e de integração da QI Tech

Como parte da assinatura das requests e das respostas é necessário que você forneça sua chave pública a nós e que nós forneçamos uma chave pública para você, assim a leitura das mensagens poderá ser feita nas duas pontas da comunicação. Além disso forneçemos uma chave única do tipo UUID que representa sua integração via API dentro de nosso sistema.

Para receber as duas chaves faça login na [plataforma QI Tech no ambiente sandbox](https://sandbox.qitech.app/). Clique em "Meu perfil", localizado no menu lateral esquerdo, depois entre na aba Integração. Após isso, insira sua chave pública no primeiro campo e clique no botão “SALVAR CHAVE”. Feito isto a chave pública e de integração da QI Tech estarão disponíveis nos campos inferiores.

![Integracao](https://storage.googleapis.com/qitech-website-documents/documentation/chaves.png)

**ATENÇÃO:** Nunca forneça sua chave privada, ela é de uso exclusivo seu e o compartilhamento da mesma no lugar da chave pública compromete a segurança de suas requests. Além disso, não compartilhe suas chaves públicas QI Tech e chave de integração pois eles são seu
meio de comunicação com nossas APIS.

<sub>
<sub>
1<a id=1></a>: Para encriptação da comunicação
2<a id=2></a>: Para autenticação e não-repúdio da informação
3<a id=3></a>: Literatura sugerida: Signing HTTP messages (https://datatracker.ietf.org/doc/draft-cavage-http-signatures/), Security Considerations for HTTP Signatures (https://web-payments.org/specs/source/http-signatures-audit/) e AWS Signing and Authenticating REST Requests (https://docs.aws.amazon.com/AmazonS3/latest/dev/RESTAuthentication.html)
4<a id=4></a>: JWT (JSON Web Token): https://jwt.io/
5<a id=5></a>: Exemplo de geração de chaves em um computador UNIX:
</sub>
</sub>


## Na prática
Com sua chave privada, chave pública da QI Tech e chave de integração em mãos podemos
começar a enviar requisições.
Toda a troca de informações entre APIs deverá utilizar o protocolo HTTPS[¹](#1) e uma assinatura  assimétrica[²](#2). Nosso modelo de implementação da assinatura é baseado no utilizado pela Amazon[³](#3), sendo a principal diferença o uso de chaves assimétricas que adicionam uma camada de não-repúdio na comunicação.

Vamos usar como um exemplo o endpoint /test para fazer um POST e validar que a autenticação funcionou:

### Request

#### Antes de performar o encode

- método: POST
- endpoint: /test
- host: api-auth.sandbox.qitech.app
- body: 
    ```json
    {
        "name": "QI Tech",
        "api_client_key": "16c8a1ec-8d75-47a1-b138-46746713b8d8",
    }
    ```

#### Depois de performar o encode

Assinando a mensagem de acordo com o estipulado pela QI resultaria em algo do tipo[⁶](#6):

- método: POST
- endpoint: /test
- host: api-auth.sandbox.qitech.app
- headers:

    ```bash
    API-CLIENT-KEY: "16c8a1ec-8d75-47a1-b138-46746713b8d8"
    Authorization: "QIT 16c8a1ec-8d75-47a1-b138-46746713b8d8:eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJzdWIiOiIxNmM4YTFlYy04ZDc1LTQ3YTEtYjEzOC00Njc0NjcxM2I4ZDgiLCJzaWduYXR1cmUiOiJQT1NUXG5kNWU2M2RlNjNkNjg0NjBkNmNlZTllN2I4ODJjM2U0M1xuYXBwbGljYXRpb24vanNvblxuV2VkLCAxNiBPY3QgMjAxOSAxNDo1MTo0NSBHTVRcbi90ZXN0In0.AZo959MUTEmfT9x_APTLZKPg9aivvjNsvCOl7rVzEkFrrMVRX0fg2Hp_eWbs60Ug9NL_EphRpNwZU9v-czyV_BmUAMBI8uJQAPd7_xACEeRjhi6QzFKuWUqk_xMzB70s7CSwGgHpeXh0OFeupHFTbwAkRkLuNAYluP0ZbT4vFrRKrdhR"
    ```
<br>

- body:
    ```json
    {
        "encoded_body": "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJuYW1lIjoiUUkgVGVjaCIsImFwaV9jbGllbnRfa2V5IjoiMTZjOGExZWMtOGQ3NS00N2ExLWIxMzgtNDY3NDY3MTNiOGQ4In0.AYHioWgjnYgvsDrYmp7zON8vLPIc6XQgO_xnMtwqV4LCL8FMejKViFPvL_Z70QKi-u8CmJW68YoQbxvDRoDAbNUOABSIHUxDXcldZk2l8_yL17yMy2hMS-mHRVutd7_-yMkhsEnYEYemEOWsGRsO3T3yey2rSX1_t7IK47ACPvpaE7Qs"
    }
    ```

Ou seja, a chamada seria reduzida a um header **`API-CLIENT-KEY`** ([chave do cliente definida em seu cadastro](?112)), um header **`Authorization`** e um body json de campo único **`encoded_body`**.

### Response

#### Antes de performar o decode


A resposta que a QI Tech responderia nessa situação seria algo semelhante a :

- headers:

    ```bash
    API-CLIENT-KEY: "16c8a1ec-8d75-47a1-b138-46746713b8d8"
    Authorization: "QIT 16c8a1ec-8d75-47a1-b138-46746713b8d8:eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJzdWIiOiIxNmM4YTFlYy04ZDc1LTQ3YTEtYjEzOC00Njc0NjcxM2I4ZDgiLCJzaWduYXR1cmUiOiJQT1NUXG5kNWU2M2RlNjNkNjg0NjBkNmNlZTllN2I4ODJjM2U0M1xuYXBwbGljYXRpb24vanNvblxuV2VkLCAxNiBPY3QgMjAxOSAxNDo1MTo0NSBHTVRcbi90ZXN0In0.AZo959MUTEmfT9x_APTLZKPg9aivvjNsvCOl7rVzEkFrrMVRX0fg2Hp_eWbs60Ug9NL_EphRpNwZU9v-czyV_BmUAMBI8uJQAPd7_xACEeRjhi6QzFKuWUqk_xMzB70s7CSwGgHpeXh0OFeupHFTbwAkRkLuNAYluP0ZbT4vFrRKrdhR"
    ```
<br>

- body:

    ```json
    {
        "encoded_body": "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJhcGlfY2xpZW50X2tleSI6IjE2YzhhMWVjLThkNzUtNDdhMS1iMTM4LTQ2NzQ2NzEzYjhkOCIsIm5hbWUiOiJRSSBUZWNoIiwic3VjY2VzcyI6IkNvbmdyYXRzISJ9.AfunfN06D38WuOPsUVhTvi19-00Jpd6Z_E7KV-Zh05nfgG55BEXQW878zwVilAmyUR8F6N9hRiAmL0djEuSahXhUAZ-bYVDbZvVb-bzYrakYEjc9gLTBE_Sk2H0NgrXCFusq9BIImEyNHwzb3aiQvDB-igcLBKEzOdIkqbfqu3lzIs_W"
    }
    ```

Ou seja, seguindo o mesmo padrão de **`API-CLIENT-KEY`** / **`Authorization`** no header e de **`encoded_body`** no body que temos na requisição.

#### Depois de performar o decode

Parabéns! 

- body:

    ```json
    {
        "api_client_key": "16c8a1ec-8d75-47a1-b138-46746713b8d8",
        "name": "QI Tech",
        "success": "Congrats!"
    }
    ```

<br>

Nas demais seções desse capítulo explicaremos como é feito o processo de encode e decode de chamadas e respostas.

<br>
<br>


<sub>
<sub>
<br>
6<a id=6></a>: Valores meramente ilustrativos. O valor da mensagem assinada deponde do cliente
<br>
</sub>
</sub>
