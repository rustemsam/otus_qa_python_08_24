# Bugs

## Bug 1

#### Name

For operation "Снабжение: Заявки - Получить список заявок" /"Снабжение: Заявки - Получить данные заявки"  we got
different error message for different projects id

#### Severity

Minor

#### Steps to reproduce

1. Perform the curl get resource requests

```curl
curl --location 'https://api.gectaro.com/v1/projects/*/resource-requests' \
--header 'Authorization: Bearer api-key' \
```

#### Expected result

1. When performing the same curl with number you'll get
   "message": "Выбранный проект недоступен.",
   And I'm expecting that we'll get the same message for anything that will pass in projects parameter

#### Actual result

1. "message": "Страница не найдена.",

________________________________________________________________________________________________________________________

## Bug 2

#### Name

For operation "Добавить заявку" request ends with 500 error

#### Severity

Major

#### Steps to reproduce

1. Perform the curl to add request resource

```curl
curl --location 'https://api.gectaro.com/v1/projects/90719/resource-requests' \
--header 'accept: */*' \
--header 'Authorization: Bearer api-key' \
--header 'Cookie: _csrf=5-MceeS0HDnWgHQ0-thHjy_atB4U1MyJ' \
--form 'project_tasks_resource_id="13486869"' \
--form 'volume="1"' \
--form 'cost="100"' \
--form 'needed_at="1720094391"' \
--form 'batch_number=""' \
--form 'batch_parent_request_id="1"' \
--form 'is_over_budget="1"'
```

#### Expected result

1. Resource request will be created and status code will be 201

#### Actual result

1. The request is failing with an 500 error and body:

```json
{
  "name": "Internal Server Error",
  "message": "Возникла внутренняя ошибка сервера.",
  "code": 0,
  "status": 500
}
```

________________________________________________________________________________________________________________________

## Bug 3

#### Name

For operation "Добавить заявку" type of some fields in response doesn't correspond with request

#### Severity

Major

#### Steps to reproduce

1. Perform the curl to add resource request

```curl
curl -X 'POST' \
  'https://api.gectaro.com/v1/projects/90719/resource-requests' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer api-key' \
  -H 'Content-Type: multipart/form-data' \
  -F 'project_tasks_resource_id=13486869' \
  -F 'volume=1' \
  -F 'cost=100' \
  -F 'needed_at=1720094391' \
  -F 'batch_number=' \
  -F 'batch_parent_request_id=' \
  -F 'is_over_budget=1'
```

#### Expected result

1. In the response we'll have the same type as we have for request, in this case:
   project_tasks_resource_id : number
   volume : number
   cost : number
   is_over_budget : integer
   needed_at : integer

#### Actual result

1. The all fields that described in expected result have type str

```json
{
  "id": 10023952,
  "project_tasks_resource_id": "13486869",
  "volume": "1",
  "cost": "100",
  "batch_number": null,
  "batch_parent_request_id": null,
  "is_over_budget": true,
  "created_at": 1727876381,
  "updated_at": 1727876381,
  "user_id": 23929,
  "needed_at": "1720094391",
  "created_by": 23929
}
```

________________________________________________________________________________________________________________________

## Bug 4

#### Name

For operation "Добавить заявку" there is no validation for the fields(cost,volume)

#### Severity

Major

#### Steps to reproduce

1. Perform the curl with negative cost

```curl
curl -X 'POST' \
  'https://api.gectaro.com/v1/projects/90719/resource-requests' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer api-key' \
  -H 'Content-Type: multipart/form-data' \
  -F 'project_tasks_resource_id=13486869' \
  -F 'volume=-10' \
  -F 'cost=-100' \
  -F 'needed_at=1720094391' \
  -F 'batch_number=' \
  -F 'batch_parent_request_id=' \
  -F 'is_over_budget=1'
```

#### Expected result

1. We'll receive 422 status code with appropriate error message

#### Actual result

1. The request resource was created with status code 201

________________________________________________________________________________________________________________________

## Bug 5

#### Name

For operation "Получить данные заявки" the format for the fields volume, cost is different compare to operation:  "
Добавить заявку"

#### Severity

Minor

#### Steps to reproduce

1. Perform the curl to add resource request

```curl
curl -X 'POST' \
  'https://api.gectaro.com/v1/projects/90719/resource-requests' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer api-key' \
  -H 'Content-Type: multipart/form-data' \
  -F 'project_tasks_resource_id=13486869' \
  -F 'volume=1' \
  -F 'cost=100' \
  -F 'needed_at=1720094391' \
  -F 'batch_number=' \
  -F 'batch_parent_request_id=' \
  -F 'is_over_budget=1'
```

2. Perform the curl to get data for created resource request from step 1

```curl
curl -X 'POST' \
  'https://api.gectaro.com/v1/projects/90719/resource-requests/10029234' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer api-key' \
  -H 'Content-Type: multipart/form-data' \
  -F 'project_tasks_resource_id=13486869' \
  -F 'volume=1' \
  -F 'cost=100' \
  -F 'needed_at=1720094391' \
  -F 'batch_number=' \
  -F 'batch_parent_request_id=' \
  -F 'is_over_budget=1'
```

#### Expected result

1. We'll receive the same format and type for the fields volume, cost, needed_at during operation "Получить данные
   заявки" , as
   we got during: "Добавить заявку"

#### Actual result

1. The format is different

```text
Type of the volume during creating "1"
Type of the cost during creating "100"
Type of the needed_at during creating "1720094391"

Type of the volume during reading "1.0000000000"
Type of the cost during reading "100.0000000000"
Type of the needed_at during reading 1720094391
```

During creating:

```json
{
  "id": 10023952,
  "project_tasks_resource_id": "13486869",
  "volume": "1",
  "cost": "100",
  "batch_number": null,
  "batch_parent_request_id": null,
  "is_over_budget": true,
  "created_at": 1727876381,
  "updated_at": 1727876381,
  "user_id": 23929,
  "needed_at": "1720094391",
  "created_by": 23929
}
```

During reading

```json
{
  "id": 10023952,
  "project_tasks_resource_id": 13486869,
  "volume": "1.0000000000",
  "cost": "100.0000000000",
  "batch_number": null,
  "batch_parent_request_id": null,
  "is_over_budget": true,
  "created_at": 1727945132,
  "updated_at": 1727945132,
  "user_id": 23929,
  "needed_at": 1720094391,
  "created_by": 23929
}
```

________________________________________________________________________________________________________________________

## Bug 6

#### Name

For operation "Изменить данные заявки" the type for parameters is different than expecting according to swagger

#### Severity

Minor

#### Steps to reproduce

1. Open the swagger:
   https://swagger.gectaro.com/#/Снабжение%3A%20Заявки/c9b0cbcc1ed81c5309173faef1f1eeef
2. Check the type for fields and perform the according curl

```curl
curl --location --request PUT 'https://api.gectaro.com/v1/projects/90719/resource-requests/10031097' \
--header 'accept: */*' \
--header 'Authorization: Bearer API-Key' \
--header 'Cookie: _csrf=EFuSV8wFCeQL6eTdonWLQBXQyCGzvj6s' \
--form 'project_tasks_resource_id="13486869"' \
--form 'volume="1"' \
--form 'cost="100"' \
--form 'needed_at="1720094391"' \
--form 'batch_number="5"' \
--form 'batch_parent_request_id="100"' \
--form 'is_over_budget="true"' \
--form 'created_at="1720094391"' \
--form 'updated_at="1820094391"' \
--form 'is_deleted="false"'
```

#### Expected result

1. We'll update the resource

#### Actual result

1. We got 422 and:

During creating:

```json
[
  {
    "field": "is_over_budget",
    "message": "Значение «сверх бюджета» должно быть равно «1» или «0»."
  }
]
```

However in the swagger it says:

```text
is_over_budget
boolean
```

________________________________________________________________________________________________________________________

## Bug 7

#### Name

For operation "Изменить данные заявки" the type for some fields in the response doesn't correspond with operation "
Добавить заявку"

#### Severity

Minor

#### Preconditions

1. Create resource request using endpoint  "Добавить заявку" and remember id from this response

#### Steps to reproduce

1. Perform the curl "Изменить данные заявки"

```curl
curl --location --request PUT 'https://api.gectaro.com/v1/projects/90719/resource-requests/10031097' \
--header 'accept: */*' \
--header 'Authorization: Bearer API-Key' \
--header 'Cookie: _csrf=EFuSV8wFCeQL6eTdonWLQBXQyCGzvj6s' \
--form 'project_tasks_resource_id="13486869"' \
--form 'volume="1"' \
--form 'cost="100"' \
--form 'needed_at="1720094391"' \
--form 'batch_number="5"' \
--form 'batch_parent_request_id="100"' \
--form 'is_over_budget="1" \
--form 'created_at="1720094391"' \
--form 'updated_at="1820094391"' \
--form 'is_deleted="false"'
```

#### Expected result

1. The response has the same type for the fields as for operation  "Изменить данные заявки"

```json
{
  "id": 10023952,
  "project_tasks_resource_id": "13486869",
  "volume": "1",
  "cost": "100",
  "batch_number": null,
  "batch_parent_request_id": null,
  "is_over_budget": true,
  "created_at": 1727876381,
  "updated_at": 1727876381,
  "user_id": 23929,
  "needed_at": "1720094391",
  "created_by": 23929
}
```

#### Actual result

1. The type for some fields is different

```json
{
  "id": 10031097,
  "project_tasks_resource_id": "13486869",
  "volume": "1",
  "cost": "100",
  "batch_number": "5",
  "batch_parent_request_id": "100",
  "is_over_budget": true,
  "created_at": "1720094391",
  "updated_at": 1728029340,
  "user_id": 23929,
  "needed_at": "1720094391",
  "created_by": 23929
}
```

For example, created_at has str instead of int

Also if you'll send only one field, for example,

```curl
curl --location --request PUT 'https://api.gectaro.com/v1/projects/90719/resource-requests/10031097' \
--header 'accept: */*' \
--header 'Authorization: Bearer API-Key' \
--header 'Cookie: _csrf=EwFZPjPRMcx8pRI_9wWtVAQdvfmEN64I' \
--form 'project_tasks_resource_id="13486869"' \
--form 'cost="100"'
```

You'll receive

```json
{
  "id": 10031097,
  "project_tasks_resource_id": "13486869",
  "volume": "1.0000000000",
  "cost": "100",
  "batch_number": 5,
  "batch_parent_request_id": 100,
  "is_over_budget": true,
  "created_at": 1720094391,
  "updated_at": 1728032057,
  "user_id": 23929,
  "needed_at": 1720094391,
  "created_by": 23929
}
```

And here batch_number, batch_parent_request_id, needed_at are int
________________________________________________________________________________________________________________________

## Bug 8

#### Name

For operation "Изменить данные заявки" there are not fields(is_deleted, deleted_at) in the response

#### Severity

Minor

#### Preconditions

1. Create resource request using endpoint  "Добавить заявку" and remember id from this response

#### Steps to reproduce

1. Perform the curl "Изменить данные заявки"

```curl
curl --location --request PUT 'https://api.gectaro.com/v1/projects/90719/resource-requests/10031097' \
--header 'accept: */*' \
--header 'Authorization: Bearer API-Key' \
--header 'Cookie: _csrf=EFuSV8wFCeQL6eTdonWLQBXQyCGzvj6s' \
--form 'deleted_at="1820094391"' \
--form 'is_deleted="true"'
```

#### Expected result

1. The response will have the fields that I passed in the request

```json
{
  "id": 10023952,
  "project_tasks_resource_id": "13486869",
  "volume": "1",
  "cost": "100",
  "batch_number": null,
  "batch_parent_request_id": null,
  "is_over_budget": true,
  "created_at": 1727876381,
  "updated_at": 1727876381,
  "user_id": 23929,
  "needed_at": "1720094391",
  "is_deleted": true,
  "deleted_at": "1820094391",
  "created_by": 23929
}
```

#### Actual result

1. The fields are not present

```json
{
  "id": 10031097,
  "project_tasks_resource_id": "13486869",
  "volume": "1.0000000000",
  "cost": "100",
  "batch_number": 5,
  "batch_parent_request_id": 100,
  "is_over_budget": true,
  "created_at": 1720094391,
  "updated_at": 1728032057,
  "user_id": 23929,
  "needed_at": 1720094391,
  "created_by": 23929
}
```

________________________________________________________________________________________________________________________

## Bug 9

#### Name

For operation "Изменить данные заявки" there is no validation for some fields, for example, is_deleted or deleted_at

#### Severity

Major

#### Preconditions

1. Create resource request using endpoint  "Добавить заявку" and remember id from this response

#### Steps to reproduce

1. Perform the curl "Изменить данные заявки"

```curl
curl --location --request PUT 'https://api.gectaro.com/v1/projects/90719/resource-requests/10031097' \
--header 'accept: */*' \
--header 'Authorization: Bearer API-Key' \
--header 'Cookie: _csrf=EFuSV8wFCeQL6eTdonWLQBXQyCGzvj6s' \
--form 'deleted_at="1820094391"' \
--form 'is_deleted="deleted"'
```

#### Expected result

1. According to the swagger this field(is_deleted) should have type boolean, and for deleted_at - integer
   so we should receive 422 and appropriate error message

#### Actual result

1. The status code is 200 and body

```json
{
  "id": 10031097,
  "project_tasks_resource_id": 13486869,
  "volume": "1.0000000000",
  "cost": "100.0000000000",
  "batch_number": 5,
  "batch_parent_request_id": 100,
  "is_over_budget": true,
  "created_at": 1720094391,
  "updated_at": 1728032057,
  "user_id": 23929,
  "needed_at": 1720094391,
  "created_by": 23929
}
```