# 网站HTTPS证书到期预警
通过curl获取网站证书信息，判断证书到期时间，如果证书到期时间到达预定的阈值`DAYS`，则通过设置的邮箱通知收件人
# 使用教程
在项目的 `Settings` -> `Secrets` -> `Actions` -> `New repository secret`，新增变量，注意区分大小写
![操作步骤1](https://raw.githubusercontent.com/Liushengxi97/static-repository/main/操作步骤1.png)
![操作步骤2](https://raw.githubusercontent.com/Liushengxi97/static-repository/main/操作步骤2.png)

# 变量说明
|   name    | 说明                     |
|:---------:|:-----------------------|
|   DAYS    | 需要提醒的过期时间              |
|  DOMAINS  | 需要提醒的域名，支持多个域名，通过`;`分割 |
| MAIL_HOST | 邮箱服务器地址，目前仅支持`STMP`协议  |
| MAIL_PASS | 邮箱授权码，非密码              |
| MAIL_USER | 邮箱地址，通过此地址发送邮件         |
| RECEIVERS | 接受邮箱的地址，支持多个域名，通过`;`分割 |

