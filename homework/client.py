import argparse

import httpx


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:5000")
    parser.add_argument("--add", nargs=2, metavar=("AUTHOR", "REVIEW"), help="Добавить отзыв")
    parser.add_argument("--author", help="Фильтр по имени")
    args = parser.parse_args()

    base = args.url.rstrip("/")

    try:
        if args.add:
            resp = httpx.post(f"{base}/api/recall", json={"author": args.add[0], "review": args.add[1]})
            print(resp.status_code, resp.json())
            return

        params = {}
        if args.author:
            params["author"] = args.author
        resp = httpx.get(f"{base}/api/recall", params=params)
        print(resp.status_code)
        for r in resp.json().get("reviews", []):
            print(f"  [{r['id']}] {r['author']}: {r['review']}")
    except httpx.HTTPStatusError as error:
        parser.exit(1, f"Сервер вернул HTTP {error.response.status_code}.\n")
    except httpx.RequestError:
        parser.exit(1, "Не удалось подключиться. Проверьте адрес и запустите Flask.\n")


if __name__ == "__main__":
    main()