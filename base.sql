-- ============================================
-- Criação das tabelas
-- ============================================

CREATE TABLE categoria (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE unidade_medida (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    sigla VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE produto (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    categoria_id BIGINT NOT NULL,
    unidade_medida_id BIGINT NOT NULL,
    quantidade_atual NUMERIC(12,3) NOT NULL DEFAULT 0,
    quantidade_minima NUMERIC(12,3) NOT NULL DEFAULT 0,
    quantidade_ideal NUMERIC(12,3) NOT NULL DEFAULT 0,
    observacao TEXT,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_produto_categoria
        FOREIGN KEY (categoria_id)
        REFERENCES categoria(id),

    CONSTRAINT fk_produto_unidade_medida
        FOREIGN KEY (unidade_medida_id)
        REFERENCES unidade_medida(id),

    CONSTRAINT chk_quantidade_atual
        CHECK (quantidade_atual >= 0),

    CONSTRAINT chk_quantidade_minima
        CHECK (quantidade_minima >= 0),

    CONSTRAINT chk_quantidade_ideal
        CHECK (quantidade_ideal >= 0)
);

CREATE TABLE compra (
    id BIGSERIAL PRIMARY KEY,
    data DATE NOT NULL,
    valor_total NUMERIC(14,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_compra_valor_total
        CHECK (valor_total >= 0)
);

CREATE TABLE item_compra (
    id BIGSERIAL PRIMARY KEY,
    compra_id BIGINT NOT NULL,
    produto_id BIGINT NOT NULL,
    quantidade NUMERIC(12,3) NOT NULL,
    valor_unitario NUMERIC(14,2) NOT NULL,
    valor_total NUMERIC(14,2) NOT NULL,

    CONSTRAINT fk_item_compra_compra
        FOREIGN KEY (compra_id)
        REFERENCES compra(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_item_compra_produto
        FOREIGN KEY (produto_id)
        REFERENCES produto(id),

    CONSTRAINT chk_item_quantidade
        CHECK (quantidade > 0),

    CONSTRAINT chk_item_valor_unitario
        CHECK (valor_unitario >= 0),

    CONSTRAINT chk_item_valor_total
        CHECK (valor_total >= 0)
);

-- ============================================
-- Índices
-- ============================================

CREATE INDEX idx_produto_categoria
    ON produto (categoria_id);

CREATE INDEX idx_produto_unidade_medida
    ON produto (unidade_medida_id);

CREATE INDEX idx_produto_nome
    ON produto (nome);

CREATE INDEX idx_compra_data
    ON compra (data);

CREATE INDEX idx_item_compra_compra
    ON item_compra (compra_id);

CREATE INDEX idx_item_compra_produto
    ON item_compra (produto_id);

-- ============================================
-- Função para atualizar updated_at
-- ============================================

CREATE OR REPLACE FUNCTION atualizar_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_produto_updated_at
BEFORE UPDATE ON produto
FOR EACH ROW
EXECUTE FUNCTION atualizar_updated_at();