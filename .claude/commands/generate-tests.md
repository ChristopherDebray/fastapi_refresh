---
name: generate-tests
description: Génère les tests unitaires pour les use cases Python
disable-model-invocation: true
---
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

## Ne pas générer de tests pour
- Repositories (couplés SQLAlchemy)
- Routes (E2E)
- DTOs (Pydantic se teste lui-même)

$ARGUMENTS