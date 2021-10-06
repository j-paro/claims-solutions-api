# claims-solutions-api
Backend API for Claims Solutions

## Data Objects
### Company
#### Fields
| Field Name | Attributes       |
| -----------| -----------------|
| Name       | Required, Unique |
| Phone      |                  |
| Address 1  |                  |
| Address 2  |                  |
| City       |                  |
| State      |                  |
| Zip        |                  |

#### JSON Request Format
```
{
    "phone": "...",
    "address_1": "...",
    "address_2": "...",
    "city": "...",
    "state": "...",
    "zip": "..."
}
```

## Features
### Company
#### Create
##### By Name
HTTP POST method --> URL/company/Company Name

#### Get
##### By Name
HTTP **GET** method --> URL/company/Company Name

##### Company List
HTTP **GET** method --> URL/companies

#### Delete
##### By Name
HTTP **DEL** method --> URL/company/Company Name
