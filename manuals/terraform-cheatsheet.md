# 🏗️ Terraform — шпаргалка по Infrastructure as Code

> **Terraform** — инструмент Infrastructure as Code (IaC) от HashiCorp.
> Декларативное описание инфраструктуры в HCL, деплой в облако.
> Документация: https://developer.hashicorp.com/terraform

---

## 🔑 Главные понятия

| Термин | Что значит |
|---|---|
| **Provider** | Плагин для облака (AWS, GCP, Azure, K8s) |
| **Resource** | Единица инфраструктуры (EC2, S3, VPC) |
| **Data source** | Чтение существующего ресурса |
| **Variable** | Входная переменная |
| **Output** | Выходное значение |
| **State (tfstate)** | Текущее состояние инфраструктуры |
| **Plan** | Что Terraform собирается сделать |
| **Apply** | Применить изменения |
| **Module** | Переиспользуемый набор ресурсов |
| **Backend** | Где хранится state (local, S3, Consul) |
| **Workspace** | Изолированный state (dev/prod) |
| **HCL** | HashiCorp Configuration Language |

---

## 🚀 Базовый цикл

```bash
terraform init          # скачать провайдеры, инициализация
terraform plan          # показать, что изменится
terraform apply         # применить изменения
terraform destroy       # удалить всю инфраструктуру
terraform fmt           # отформатировать .tf файлы
terraform validate      # проверить синтаксис
terraform output        # показать outputs
terraform show          # текущее state
terraform state list    # список ресурсов в state
```

### Установка
```bash
sudo pacman -S terraform       # Arch / CachyOS
sudo apt install terraform     # Debian/Ubuntu
brew install terraform         # macOS

# tfenv (управление версиями)
git clone https://github.com/tfutils/tfenv.git ~/.tfenv
export PATH="$HOME/.tfenv/bin:$PATH"
tfenv install 1.7.0
tfenv use 1.7.0
```

---

## 📝 Структура проекта

```
project/
├── main.tf              # ресурсы
├── variables.tf         # входные переменные
├── outputs.tf           # выходные значения
├── providers.tf         # провайдеры
├── backend.tf           # конфигурация state
├── terraform.tfvars     # значения переменных
├── versions.tf          # версии Terraform и провайдеров
├── locals.tf            # локальные переменные
└── modules/             # свои модули
    └── vpc/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

### Минимальный пример
```hcl
# versions.tf
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# providers.tf
provider "aws" {
  region = "us-east-1"
  profile = "default"
}

# main.tf
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  tags = {
    Name = "WebServer"
  }
}

# outputs.tf
output "instance_ip" {
  value = aws_instance.web.public_ip
}
```

---

## 🔤 Синтаксис HCL

### Блоки
```hcl
resource "aws_instance" "web" {     # тип, имя
  ami           = "ami-123"
  instance_type = "t3.micro"

  tags = {
    Name        = "web"
    Environment = "prod"
  }
}
```

### Переменные (variables.tf)
```hcl
variable "region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region"
}

variable "instance_count" {
  type    = number
  default = 2
}

variable "tags" {
  type    = map(string)
  default = {
    Project = "myapp"
    Owner   = "ops"
  }
}

variable "environments" {
  type    = list(string)
  default = ["dev", "staging", "prod"]
}

variable "instance_type" {
  type    = string
  validation {
    condition     = contains(["t3.micro", "t3.small", "t3.medium"], var.instance_type)
    error_message = "Must be t3.micro, t3.small, or t3.medium."
  }
}

# sensitive (не показывается в plan)
variable "db_password" {
  type      = string
  sensitive = true
}
```

### Использование переменных
```hcl
provider "aws" {
  region = var.region
}

resource "aws_instance" "web" {
  count         = var.instance_count       # создать N
  instance_type = var.instance_type
  tags          = var.tags
}
```

### `terraform.tfvars`
```hcl
region         = "eu-west-1"
instance_count = 3
db_password    = "supersecret"
```

### Outputs
```hcl
output "instance_ips" {
  value       = aws_instance.web[*].public_ip
  description = "Public IPs of instances"
}

output "vpc_id" {
  value = aws_vpc.main.id
}

output "db_endpoint" {
  value     = aws_db.main.endpoint
  sensitive = true
}
```

### Locals
```hcl
locals {
  common_tags = {
    Project   = "myapp"
    ManagedBy = "terraform"
  }
  instance_name = "web-${var.environment}"
}

resource "aws_instance" "web" {
  tags = merge(local.common_tags, { Name = local.instance_name })
}
```

---

## 🔄 Resource и Data source

### Resource (создать)
```hcl
resource "aws_s3_bucket" "data" {
  bucket = "my-unique-bucket-name"
  tags   = { Name = "Data bucket" }
}

resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  versioning_configuration {
    status = "Enabled"
  }
}
```

### Data source (прочитать существующее)
```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]    # Canonical
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

resource "aws_instance" "web" {
  ami = data.aws_ami.ubuntu.id
}
```

### Ссылки между ресурсами
```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "web" {
  vpc_id     = aws_vpc.main.id           # ссылка
  cidr_block = "10.0.1.0/24"
}

resource "aws_instance" "web" {
  subnet_id = aws_subnet.web.id          # ссылка
}
```

---

## 🔁 Meta-аргументы

### count
```hcl
resource "aws_instance" "web" {
  count         = 3
  instance_type = "t3.micro"
  tags = {
    Name = "web-${count.index}"
  }
}
# Доступ: aws_instance.web[0], aws_instance.web[1], aws_instance.web[2]
```

### for_each
```hcl
resource "aws_instance" "web" {
  for_each = toset(["web-1", "web-2", "web-3"])
  tags = {
    Name = each.key
  }
  instance_type = "t3.micro"
}

# Map для разных конфигов
variable "instances" {
  type = map(object({
    instance_type = string
    env           = string
  }))
  default = {
    web = { instance_type = "t3.micro", env = "prod" }
    db  = { instance_type = "t3.large", env = "prod" }
  }
}

resource "aws_instance" "server" {
  for_each      = var.instances
  instance_type = each.value.instance_type
  tags          = { Name = each.key, Env = each.value.env }
}
```

### depends_on
```hcl
resource "aws_instance" "app" {
  # ...
  depends_on = [
    aws_iam_role_policy.example,
  ]
}
```

### lifecycle
```hcl
resource "aws_instance" "web" {
  # ...

  lifecycle {
    create_before_destroy = true       # сначала создать, потом удалить
    prevent_destroy       = true       # запретить удаление
    ignore_changes        = [tags]     # не управлять этими полями
    replace_triggered_by  = [aws_security_group.web.id]
  }
}
```

### provisioner (не рекомендуется!)
```hcl
resource "aws_instance" "web" {
  # ...

  provisioner "remote-exec" {
    inline = [
      "sudo apt update",
      "sudo apt install -y nginx",
    ]
    connection {
      host        = self.public_ip
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/id_rsa")
    }
  }

  provisioner "local-exec" {
    command = "echo ${self.public_ip} > inventory.txt"
  }
}
```
> Предпочтительнее: cloud-init, Ansible, scripts в образе (Packer).

---

## 🎛️ dynamic blocks
```hcl
resource "aws_security_group" "web" {
  name = "web-sg"

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = "tcp"
      cidr_blocks = ingress.value.cidrs
    }
  }
}
```

---

## 📦 Modules

### Использование модуля
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  tags = {
    Environment = "prod"
  }
}

output "vpc_id" {
  value = module.vpc.vpc_id
}
```

### Свой модуль
```
modules/web_server/
├── main.tf
├── variables.tf
└── outputs.tf
```

```hcl
# modules/web_server/variables.tf
variable "instance_count" {
  type    = number
  default = 1
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

# modules/web_server/main.tf
resource "aws_instance" "web" {
  count         = var.instance_count
  instance_type = var.instance_type
  ami           = "ami-123"
}

# modules/web_server/outputs.tf
output "instance_ids" {
  value = aws_instance.web[*].id
}
```

Использование:
```hcl
module "web_servers" {
  source         = "./modules/web_server"
  instance_count = 3
  instance_type  = "t3.small"
}
```

---

## 💾 Backend (хранение state)

### Локально (по умолчанию)
State в `terraform.tfstate` (НЕ КОММИТИТЬ В GIT!).

### S3 backend (рекомендуется для команд)
```hcl
terraform {
  backend "s3" {
    bucket         = "my-tfstate-bucket"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"   # для блокировки
    encrypt        = true
  }
}
```

### Другие backend'ы
- **S3** (+ DynamoDB для lock)
- **Azure Blob**
- **GCS**
- **Consul**
- **HTTP** (Terraform Cloud, Atlantis)
- **remote** (Terraform Cloud)

### Чувствительные данные в state
State содержит ВСЕ значения, включая секреты!
- Используйте `sensitive = true` (скрывает из plan, но не из state).
- Backend с шифрованием (S3 SSE).
- Ограниченный доступ к state-файлу.
- **Vault** для секретов.

---

## 🌍 Workspaces

```bash
terraform workspace new prod
terraform workspace select prod
terraform workspace list
terraform workspace show
terraform workspace delete dev
```

```hcl
# Использование workspace в конфиге
resource "aws_instance" "web" {
  tags = {
    Environment = terraform.workspace
  }
}

# Разный размер по workspace
locals {
  instance_type = terraform.workspace == "prod" ? "t3.large" : "t3.micro"
}
```

> Осторожно: workspaces = разные state в одном backend. Не всегда удобно для разных окружений.

---

## 🔧 State management

```bash
terraform state list                         # список ресурсов
terraform state show aws_instance.web        # детали ресурса
terraform state pull                         # вывести state в JSON
terraform state mv old.name new.name         # переименовать
terraform state rm aws_instance.old          # удалить из state (НЕ ресурс)
terraform state replace-provider hashicorp/aws hashicorp/awsnew
terraform import aws_instance.web i-12345    # импортировать существующее
terraform refresh                            # обновить state
terraform taint aws_instance.web             # пометить для пересоздания
terraform untaint aws_instance.web
```

### import (для существующей инфры)
```bash
terraform import aws_s3_bucket.mybucket my-bucket-name
terraform import aws_instance.web i-0123456789abcdef
```
Затем нужно описать ресурс вручную в `.tf`, чтобы state совпал с кодом.

---

## 📋 Управление переменными

```bash
# Через CLI
terraform apply -var="region=eu-west-1"
terraform apply -var-file="prod.tfvars"
terraform apply -var="instance_count=3"

# Из env-переменных (TF_VAR_<name>)
export TF_VAR_db_password="secret"
terraform apply

# auto.tfvars — автоматически подхватывается
echo 'region = "eu-west-1"' > prod.auto.tfvars

# Секреты — через vault, ssm, секреты
data "aws_ssm_parameter" "db_password" {
  name = "/myapp/db/password"
}
```

---

## 🛠️ Провайдеры (популярные)

| Provider | Что |
|---|---|
| **aws** | Amazon Web Services |
| **azurerm** | Microsoft Azure |
| **google** | Google Cloud |
| **kubernetes** | K8s |
| **helm** | Helm charts |
| **docker** | Docker |
| **github** | GitHub |
| **gitlab** | GitLab |
| **null** | Локальные команды |
| **random** | Случайные значения |
| **local** | Локальные файлы |
| **tls** | Сертификаты |
| **vault** | HashiCorp Vault |
| **consul** | HashiCorp Consul |
| **datadog** | Datadog |
| **pagerduty** | PagerDuty |

---

## 🚀 Полный пример: VPC + EC2 + RDS

```hcl
# main.tf
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
}

resource "aws_security_group" "web" {
  name   = "web-sg"
  vpc_id = aws_vpc.main.id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web.id]
  user_data              = file("user_data.sh")
  tags                   = { Name = "web-server" }
}

resource "aws_db_instance" "main" {
  allocated_storage   = 20
  engine              = "postgres"
  engine_version      = "16"
  instance_class      = "db.t3.micro"
  name                = "mydb"
  username            = "postgres"
  password            = var.db_password
  skip_final_snapshot = true
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}
```

---

## 🪤 Частые ошибки

1. **State в git** — утечка секретов, конфликты. Используйте backend.
2. **`terraform apply -auto-approve` в CI** — без review, опасно.
3. **Manual changes** — ручные правки ломают state.
4. **`force-unlock` без причины** — race condition.
5. **Большие monolithic state** — медленно, конфликты.
6. **Провайдер не закреплён** в `required_providers` — ломается совместимость.
7. **`count` и `for_each` на пустых коллекциях** — ресурс не создаётся.
8. **`depends_on` для ресурсов** — чаще всего не нужен (Terraform сам строит граф).
9. **provisioner для конфигурации** — используйте cloud-init / Ansible.
10. **`terraform destroy` без plan** — удаляет ВСЁ.

---

## 🆚 Terraform vs Alternatives

| | Terraform | Pulumi | CloudFormation | Ansible |
|---|---|---|---|---|
| Язык | HCL | TS/Python/Go | JSON/YAML | YAML |
| Подход | Декларативный | Декларативный | Декларативный | Процедурный |
| Мульти-cloud | ✅ | ✅ | Только AWS | ✅ |
| State | Свой | Свой | AWS-managed | Без state |
| Open-source | ✅ (с 2023 — BSL) | ✅ | ✅ | ✅ |

---

## 🔗 Полезные ссылки

- Документация: https://developer.hashicorp.com/terraform
- Learn: https://developer.hashicorp.com/terraform/tutorials
- Registry (провайдеры/модули): https://registry.terraform.io
- Best Practices: https://www.terraform-best-practices.com
- Awesome Terraform: https://github.com/shuaibiyy/awesome-terraform
- Terraform AWS modules: https://github.com/terraform-aws-modules
- tfsec (security scanner): https://github.com/aquasecurity/tfsec
- tflint: https://github.com/terraform-linters/tflint
- Terragrunt (DRY): https://terragrunt.gruntwork.io
- Atlantis (PR automation): https://www.runatlantis.io

---

## 💡 Полезные советы

1. **`terraform fmt` + `terraform validate`** — перед коммитом.
2. **`terraform plan`** — ВСЕГДА смотрите перед apply.
3. **State в backend** (S3+DynamoDB), НЕ в git.
4. **Modules** — для переиспользования и стандартов.
5. **variables.tf + tfvars** — для разных окружений.
6. **`required_version` + `required_providers`** — фиксируйте версии.
7. **`data` sources** — для чтения существующих ресурсов.
8. **`for_each` вместо `count`** — если элементы не числовые.
9. **`locals`** — для вычисляемых значений.
10. **`lifecycle.prevent_destroy`** — для критичных ресурсов.
11. **Terragrunt** — для DRY (один конфиг, разные окружения).
12. **Atlantis / Terraform Cloud** — для PR-based деплоя.
13. **tfsec / tflint / checkov** — статический анализ.
14. **`terraform import`** — для существующей инфры.
15. **State isolation** — отдельный state на окружение/команду.

---

*Сгенерировано как шпаргалка. Terraform — стандарт IaC —
углубляйтесь через https://developer.hashicorp.com/terraform*
