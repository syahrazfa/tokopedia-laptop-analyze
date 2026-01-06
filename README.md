## Endpoint

POST https://gql.tokopedia.com/graphql/SearchProductV5Query

## Purpose

Provides Tokopedia’s canonical public product feed for search result pages.
Returns full product, seller, stock, and price information used by Tokopedia frontend.

## Request

Method: POST  
Content-Type: application/json  
Required Headers:
- User-Agent
- Content-Type

## Canonical Truth Fields

| Canonical Meaning | JSON Path |
|------------------|----------|
| product_id | data.searchProductV5.products[].id |
| product_name | data.searchProductV5.products[].name |
| product_url | data.searchProductV5.products[].url |
| seller_id | data.searchProductV5.products[].shop.id |
| seller_name | data.searchProductV5.products[].shop.name |
| seller_city | data.searchProductV5.products[].shop.city |
| stock | data.searchProductV5.products[].stock |
| image | data.searchProductV5.products[].mediaURL.image300 |
| price | data.searchProductV5.products[].price |

## Notes

- Endpoint returns GraphQL JSON.
- This feed is the primary source of public Tokopedia product truth.
- All product price history will be derived from this endpoint.
