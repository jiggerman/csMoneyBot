from fake_useragent import UserAgent
import requests
import json

us = UserAgent()

"""
type 1: Case Key
type 2: Knife 
type 3: Штурмовые винтовки
type 4: AWP 
type 5: пистолеты 
type 6: Пистолеты-пулемёты 
type 7: Дробовики
type 8: Пулемёты
"""


def collect_data(gun_type=1, min_price=0, max_price=10**10, discount=0.15):

    #response = requests.get(
    #    url='https://cs.money/1.0/market/sell-orders?limit=60&maxPrice=120&offset=60'
    #    https://cs.money/1.0/market/sell-orders?limit=60&maxPrice=120&minPrice=5&offset=60&type=3,
    #    headers={'user-agent': f'{us.random}'}
    #)
    #with open('result.json', 'w', encoding='utf8') as file:
    #    json.dump(response.json(), file, indent=4, ensure_ascii=False)

    offset = 0
    up_offset = 60
    result = []
    count = 0
    flag = True

    while flag:
        for item in range(offset, offset + up_offset, 60):

            url = f'https://cs.money/1.0/market/sell-orders?limit=60&maxPrice={max_price}&minPrice={min_price}&offset={item}&type={gun_type}'
            response = requests.get(
                url=url,
                headers={'user-agent': f'{us.random}'}
            )

            offset += up_offset

            data = response.json()

            if data == {"errors":[{"code":400,"details":["offset is invalid"]}]}:
                flag = False
                break

            items = data.get('items')

            for i in items:
                pricing = i.get('pricing')
                if pricing.get('discount') is not None and pricing.get('discount') > discount:
                    item_full_name = i.get('asset').get('names').get('full')
                    item_3d_link = i.get('links').get('3d')
                    item_price = pricing.get('computed')
                    item_discount = pricing.get('discount')

                    result.append(
                        {
                            'full_name': item_full_name,
                            '3d': item_3d_link,
                            'discount': item_discount,
                            'price': item_price,
                        }
                    )

            count += 1
            print(f'Page: {count}')
            print(url)

            if len(items) < 50:
                flag = False
                break

    with open('result.json', 'w', encoding='utf8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    print(len(result))


def main():
    collect_data()


if __name__ == '__main__':
    main()