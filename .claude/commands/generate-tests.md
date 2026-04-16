---
name: generate-tests
description: Génère les tests unitaires pour les use cases Python
disable-model-invocation: true
---
<!-- 
USAGE:
  /generate-tests                                                        → fichiers staged
  /generate-tests server/app/module/user/application/use_cases/         → dossier entier
  /generate-tests server/app/module/user/application/use_cases/create_user_use_case.py   → fichier unique
-->
Phrases courtes. Pas de politesses. Termes techniques intacts.

## Déterminer les fichiers cibles

Si $ARGUMENTS contient des chemins → utilise ces chemins comme cibles.
Sinon → récupère les fichiers staged : `git diff --cached --name-only --diff-filter=AM`

## Pour chaque fichier *.py trouvé

1. Lis le fichier et identifie les méthodes publiques et leurs cas d'erreur
2. Génère tests/unit/<même chemin relatif depuis app/>/test_<nom_fichier>.py
3. Structure par test :
   - Given : MagicMock() pour les ports, instanciation réelle du use case et des DTOs
   - When : appel de la méthode testée
   - Then : assert sur le résultat + assert_called_once_with sur les mocks
4. Couvre : happy path + chaque HTTPException possible (404, 409, 401)
5. Ne jamais mocker les DTOs — instancie-les avec des valeurs réelles
6. MagicMock implémente Protocol implicitement, pas besoin de spec=

## Règles de structure pytest

### `@pytest.mark.parametrize`
Utilise dès que 2+ tests testent la même logique avec des inputs différents.
Exemples typiques :
- Même erreur (401) déclenchée par plusieurs causes (user not found, bad password)
- Validation de champs : plusieurs valeurs invalides pour le même champ
- Même happy path avec des rôles ou états différents

Format avec IDs pour lisibilité dans la sortie pytest :
```python
@pytest.mark.parametrize("email,expected_status", [
    ("", 422),
    ("not-an-email", 422),
], ids=["empty_email", "invalid_format"])
def test_create_user_invalid_email(self, use_case, email, expected_status): ...
```

Ne pas utiliser parametrize si les scénarios ont des mocks différents — sépare les tests.

### `pytest.raises`
Toujours utiliser `pytest.raises` pour tester les HTTPException :
```python
with pytest.raises(HTTPException) as exc_info:
    use_case.execute(dto)
assert exc_info.value.status_code == 404
assert exc_info.value.detail == "Entity not found"
```

### Fixtures et `conftest.py`
- Fixtures propres au fichier → définies dans le fichier test
- Fixtures partagées entre plusieurs fichiers d'un même module → `conftest.py` dans le dossier commun
- Scope par défaut (`function`) sauf si fixture coûteuse et stateless (`scope="module"`)

### Nommage des tests
Pattern : `test_<méthode>_<scénario>_<résultat_attendu>`
Exemples :
- `test_execute_happy_path`
- `test_execute_user_not_found_raises_404`
- `test_execute_duplicate_email_raises_409`

## Ne pas générer de tests pour
- Repositories (couplés SQLAlchemy)
- Routes (E2E)
- DTOs (Pydantic se teste lui-même)

$ARGUMENTS