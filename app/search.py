from app.models import VaultItem

def search_items(items:list[VaultItem],query:str,category:str|None=None,sort_by:str="score")->list[tuple[int, VaultItem]]:
    query=query.lower().strip()
    results=[]

    for item in items:
        if category is not None and item.category != category:
            continue

        score = 0

        if query in item.title.lower():
            score += 3

        if query in item.content.lower():
            score += 1

        if any(query in tag.lower() for tag in item.tags):
            score += 2

        if score > 0:
            results.append((score, item))

    if sort_by == "recent":
            results.sort(key=lambda result: result[1].created_at,reverse=True)  
    else:
         results.sort(key=lambda result: result[0], reverse=True)

    return results    