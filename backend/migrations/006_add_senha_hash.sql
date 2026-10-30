-- Não apaga usuários existentes; senhas antigas não são recuperáveis.
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS senha_hash TEXT;