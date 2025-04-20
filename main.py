from flask import Flask, request, render_template
import psycopg2
from config import config

app = Flask(__name__)


#Arquivo .py que executa os mesmos comandos apresentados no .sql no banco de dados da cafeteria, estando ele já criado no PostgreSQL

def create_tables():
      #Cria as tabelas no banco de dados.

      commands = (
            '''
            CREATE TABLE Clientes (
                  ID_cliente INT PRIMARY KEY,
                  pNome VARCHAR(100) NOT NULL,
                  uNome VARCHAR(100) NOT NULL,
                  Endereco VARCHAR(255),
                  Telefone VARCHAR(20) UNIQUE NOT NULL,
                  Email VARCHAR(100) UNIQUE
            )
            ''',
            
            '''
            CREATE TABLE Mesa_Atendimento (
                  ID_mesa INT PRIMARY KEY,
                  NumeroMesa INT NOT NULL,
                  StatusMesa VARCHAR(50)
            )
            ''',
            
            '''
            CREATE TABLE Produtos (
                  ID_produto INT PRIMARY KEY,
                  NomeProduto VARCHAR(100) UNIQUE NOT NULL,
                  Preco DECIMAL(10, 2) NOT NULL,
                  Categoria VARCHAR(50) NOT NULL,
                  Disponibilidade BOOLEAN NOT NULL
            )
            ''',
            
            '''
            CREATE TABLE Funcionarios (
                  ID_funcionario INT PRIMARY KEY,
                  pNome VARCHAR(100) NOT NULL,
                  uNome VARCHAR(50) NOT NULL,
                  genero VARCHAR(1) NOT NULL,
                  DataNascimento DATE CHECK (DataNascimento <= current_date - interval '18 years') NOT NULL,
                  telefone VARCHAR(100) UNIQUE NOT NULL,
                  email VARCHAR(100) UNIQUE,
                  DataContratacao DATE NOT NULL,
                  Salario DECIMAL(10, 2),
                  n_dependentes INT
            )
            ''',      
              
            '''
            CREATE TABLE Pedidos (
                  ID_pedido INT PRIMARY KEY,
                  DataHoraPedido TIMESTAMP NOT NULL,
                  ID_cliente INT NOT NULL,
                  StatusPedido VARCHAR(50) NOT NULL,
                  ID_mesa INT NOT NULL,
                  ID_funcionario INT NOT NULL,
                  FOREIGN KEY (ID_cliente) REFERENCES Clientes(ID_cliente),
                  FOREIGN KEY (ID_mesa) REFERENCES Mesa_Atendimento(ID_mesa),
                  FOREIGN KEY (ID_funcionario) REFERENCES Funcionarios(ID_funcionario)
            )
            ''',
            
            '''
            CREATE TABLE Itens_Pedido (
                  ID_item INT PRIMARY KEY,
                  ID_pedido INT NOT NULL,
                  ID_produto INT NOT NULL,
                  Quantidade INT NOT NULL,
                  PrecoUnitario DECIMAL(10, 2) NOT NULL,
                  FOREIGN KEY (ID_pedido) REFERENCES Pedidos(ID_pedido),
                  FOREIGN KEY (ID_produto) REFERENCES Produtos(ID_produto)
            )
            ''',
            
            '''
            CREATE TABLE Fornecedores (
                  ID_fornecedor INT PRIMARY KEY,
                  NomeFornecedor VARCHAR(100) UNIQUE NOT NULL,
                  ContatoFornecedor VARCHAR(100) UNIQUE NOT NULL
            )
            ''',
            
            '''
            CREATE TABLE Estoque (
                  EstoqueID INT PRIMARY KEY,
                  QuantidadeEmEstoque INT NOT NULL,
                  DataAtualizacaoEstoque TIMESTAMP,
                  ID_fornecedor INT NOT NULL,
                  ID_produto INT,
                  FOREIGN KEY (ID_produto) REFERENCES Produtos(ID_produto),
                  FOREIGN KEY (ID_fornecedor) REFERENCES Fornecedores(ID_fornecedor)
            )
            ''',
            
            '''
            CREATE TABLE Transacoes_Financeiras (
                  ID_transacao INT PRIMARY KEY,
                  TipoTransacao VARCHAR(50) NOT NULL,
                  Valor DECIMAL(10, 2) NOT NULL,
                  DataHoraTransacao TIMESTAMP NOT NULL,
                  ID_pedido INT,
                  ID_cliente INT,
                  FOREIGN KEY (ID_pedido) REFERENCES Pedidos(ID_pedido),
                  FOREIGN KEY (ID_cliente) REFERENCES Clientes(ID_cliente)
            )          
            ''',
            
            '''
            CREATE TABLE AvaliacoesComentarios (
                  ID_avaliacao INT PRIMARY KEY,
                  ID_cliente INT NOT NULL,
                  Classificacao INT,
                  Comentario TEXT,
                  DataAvaliacao DATE NOT NULL,
                  FOREIGN KEY (ID_cliente) REFERENCES Clientes(ID_cliente)
            )
            '''
      )

      conn = None
      try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            for command in commands:
                  cur.execute(command)
            cur.close()
            conn.commit()
            
      except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            
      finally:
            if conn is not None:
                  conn.close()

def insert_data():
      #Insere dados nas tabelas.
      commands = (
            '''
            INSERT INTO Clientes (ID_cliente, pNome, uNome, Endereco, Telefone, Email)
            VALUES
                  (101, 'João', 'Silva', 'Rua A, 123', '555-1234', 'joao.silva@email.com'),
                  (142, 'Maria', 'Santos', 'Avenida B, 456', '555-5678', 'maria.santos@email.com'),
                  (300, 'Pedro', 'Ferreira', 'Rua C, 789', '555-9876', 'pedro.ferreira@email.com'),
                  (411, 'Ana', 'Oliveira', 'Avenida D, 789', '555-4321', 'ana.oliveira@email.com'),
                  (157, 'Carlos', 'Sousa', 'Rua E, 456', '555-8765', 'carlos.sousa@email.com'),
                  (222, 'Mariana', 'Silva', 'Rua F, 321', '555-2345', 'mariana.silva@email.com'),
                  (007, 'Lucas', 'Ribeiro', 'Avenida G, 123', '555-7890', 'lucas.ribeiro@email.com'),
                  (999, 'Camila', 'Fernandes', 'Rua H, 567', '555-3456', 'camila.fernandes@email.com'),
                  (070, 'Henrique', 'Brito', NULL, '1234-5678', 'henrique.brito@yahoo.com')
            ''',
            
            '''
            INSERT INTO Produtos (ID_produto, NomeProduto, Preco, Categoria, Disponibilidade)
            VALUES
                  (001, 'Café Espresso', 3.50, 'Bebida', true),
                  (002, 'Cappuccino', 4.50, 'Bebida', true),
                  (003, 'Bolo de Chocolate', 5.00, 'Comida', true),
                  (004, 'Café Latte', 4.00, 'Bebida', true),
                  (005, 'Croissant', 3.75, 'Comida', false),
                  (006, 'Chá de Camomila', 2.50, 'Bebida', true),
                  (007, 'Sanduíche de Frango', 6.50, 'Comida', true),
                  (008, 'Muffin de Blueberry', 4.25, 'Comida', false)
            ''',
            
            '''
            INSERT INTO Funcionarios (ID_funcionario, pNome, uNome, genero, DataNascimento, telefone, email, DataContratacao, Salario, n_dependentes)
            VALUES

                  (181, 'Felipe', 'Ribeiro', 'M', '2002-07-30', '38991731871', NULL, '2020-04-30', 2640.00, 0),
                  (1, 'Ana', 'Oliveira', 'F', '1990-03-15', '67991488726', 'ana.oliveira@email.com', '2019-09-15', 2500.00, 0),
                  (2, 'Lucas', 'Santos', 'M', '1995-01-20', '62992191896', 'lucas.santos@email.com', '2019-10-01', 1800.00, 1),
                  (3, 'Carla', 'Silveira', 'F', '1997-07-10', '31991049497', 'carla.silveira@email.com', '2020-02-18', 2600.00, 0),
                  (4, 'Pedro', 'Rocha', 'M', '1992-05-25', '94996631118', 'pedro.rocha@email.com', '2019-11-30', 2700.00, 2),
                  (5, 'Mariana', 'Lima', 'F', '1993-08-12', '62992426888', 'mariana.lima@email.com', '2021-03-22', 2900.00, 1),
                  (6, 'Rodrigo', 'Fernandes', 'M', '1998-04-05', '38999195166', 'rodrigo.fernandes@email.com', '2020-05-10', 2750.00, 3),
                  (7, 'Isabela', 'Pereira', 'F', '1994-12-03', '53984558046', 'isabela.pereira@email.com', '2019-12-10', 2550.00, 0),
                  (8, 'Gustavo', 'Almeida', 'M', '1991-09-20', '1140042985', 'gustavo.almeida@email.com', '2020-08-15', 2650.00, 1)
            ''',
            
            '''
            INSERT INTO Mesa_Atendimento (ID_mesa, NumeroMesa, StatusMesa)
            VALUES
                  (1, 101, 'Disponível'),
                  (2, 102, 'Ocupada'),
                  (3, 103, 'Disponível'),
                  (4, 104, 'Ocupada'),
                  (5, 105, 'Disponível'),
                  (6, 106, 'Disponível'),
                  (7, 107, 'Ocupada'),
                  (8, 108, 'Ocupada')
            ''',
            
            '''
            INSERT INTO Pedidos (ID_pedido, DataHoraPedido, ID_cliente, StatusPedido, ID_mesa, ID_funcionario)
            VALUES
                  (1, '2023-09-17 10:30:00', 007, 'Concluido', 3, 181),
                  (2, '2023-09-17 11:15:00', 411, 'Concluido', 2, 181),
                  (3, '2023-09-17 11:32:00', 411, 'Concluido', 2, 2),
                  (4, '2023-09-17 13:30:00', 300, 'Concluido', 5, 1),
                  (5, '2023-09-17 14:45:00', 101, 'Concluido', 4, 8),
                  (6, '2023-09-17 15:20:00', 222, 'Concluido', 6, 7),
                  (7, '2023-09-17 16:10:00', 999, 'Em andamento', 8, 6),
                  (8, '2023-09-17 16:20:00', 157, 'Concluido', 7, 3),
                  (9, '2023-09-17 17:00:00', 157, 'Em andamento', 7, 5),
                  (10, '2023-09-17 17:10:00', 142, 'Em andamento', 8, 4);
            ''',
            
            '''
            INSERT INTO AvaliacoesComentarios (ID_avaliacao, ID_cliente, Classificacao, Comentario, DataAvaliacao)
            VALUES
                  (1, 157, 5, 'Excelente serviço!', '2023-09-17'),
                  (2, 142, 4, 'Muito bom!', '2023-09-16'),
                  (3, 007, 3, 'Atendimento regular.', '2023-09-15'),
                  (4, 999, 5, 'Adorei a comida!', '2023-09-14'),
                  (5, 222, 4, 'Serviço rápido.', '2023-09-13'),
                  (6, 300, 2, 'Não gostei do café.', '2023-09-12'),
                  (7, 411, 4, 'Ambiente agradável.', '2023-09-11'),
                  (8, 101, 3, 'Preços um pouco altos.', '2023-09-10'),
                  (9, 157, 5, 'Sempre volto aqui!', '2023-09-09'),
                  (10, 142, 4, 'Café delicioso.', '2023-09-08'),
                  (11, 007, 3, 'Atendimento demorado.', '2023-09-07'),
                  (12, 999, 4, 'Bom custo-benefício.', '2023-09-06'),
                  (13, 222, 5, 'Ótimo lugar para relaxar.', '2023-09-05'),
                  (14, 300, 2, 'Não recomendo.', '2023-09-04'),
                  (15, 411, 4, 'Comida saborosa.', '2023-09-03'),
                  (16, 101, 3, 'Esperava mais.', '2023-09-02'),
                  (17, 157, 5, 'Serviço impecável!', '2023-09-01'),
                  (18, 142, 4, 'Mesa confortável.', '2023-08-31'),
                  (19, 007, 3, 'Preços justos.', '2023-08-30'),
                  (20, 999, 5, 'Atendimento excelente!', '2023-08-29'),
                  (21, 222, 4, 'Bom lugar para estudar.', '2023-08-28'),
                  (22, 300, 2, 'Precisa melhorar.', '2023-08-27'),
                  (23, 411, 4, 'Voltaria novamente.', '2023-08-26'),
                  (24, 101, 3, 'Ambiente acolhedor.', '2023-08-25'),
                  (25, 157, 5, 'Recomendo a todos!', '2023-08-24'),
                  (26, 142, 4, 'Excelente café!', '2023-08-23'),
                  (27, 007, 3, 'Pode melhorar.', '2023-08-22'),
                  (28, 999, 5, 'Adorei o cardápio!', '2023-08-21'),
                  (29, 222, 4, 'Ótimo atendimento.', '2023-08-20'),
                  (30, 300, 2, 'Não gostei do serviço.', '2023-08-19')
            ''',
            
            '''
            INSERT INTO Itens_Pedido (ID_item, ID_pedido, ID_produto, Quantidade, PrecoUnitario)
            VALUES
                  (1, 1, 1, 2, 3.50),
                  (2, 1, 3, 1, 5.00),
                  (3, 2, 2, 2, 4.50),
                  (4, 2, 4, 1, 4.00),
                  (5, 3, 1, 3, 3.50),
                  (6, 4, 3, 1, 5.00),
                  (7, 5, 2, 2, 4.50),
                  (8, 6, 4, 1, 4.00)
            ''',
            
            '''
            INSERT INTO Fornecedores (ID_fornecedor, NomeFornecedor, ContatoFornecedor)
            VALUES
                  (1, 'Fornecedor A', 'Contato A'),
                  (2, 'Fornecedor B', 'Contato B'),
                  (3, 'Fornecedor C', 'Contato C'),
                  (4, 'Fornecedor D', 'Contato D')
            ''',
            
            '''
            INSERT INTO Estoque (EstoqueID, ID_produto, QuantidadeEmEstoque, DataAtualizacaoEstoque, ID_fornecedor)
            VALUES
                  (1, 1, 50, '2023-09-17 10:00:00', 1),
                  (2, 2, 40, '2023-09-17 10:05:00', 2),
                  (3, 3, 30, '2023-09-17 10:10:00', 1),
                  (4, 4, 20, '2023-09-17 10:15:00', 3),
                  (5, 5, 0, '2023-09-17 10:20:00', 2),
                  (6, 6, 70, '2023-09-17 10:25:00', 1),
                  (7, 7, 45, '2023-09-17 10:30:00', 4),
                  (8, 8, 0, '2023-09-17 10:35:00', 3)
            ''',
            
            '''
            INSERT INTO Transacoes_Financeiras (ID_transacao, TipoTransacao, Valor, DataHoraTransacao, ID_pedido, ID_cliente)
            VALUES
                  (1, 'Venda', 25.00, '2023-09-17 10:45:00', 8, 157),
                  (2, 'Venda', 18.50, '2023-09-17 11:30:00', 6, 222),
                  (3, 'Compra', -120.00, '2023-09-17 12:15:00', NULL, NULL),
                  (4, 'Venda', 30.00, '2023-09-17 13:00:00', 2, 411),
                  (5, 'Compra', -80.00, '2023-09-17 14:00:00', NULL, NULL),
                  (6, 'Venda', 42.00, '2023-09-17 14:45:00', 4, 300),
                  (7, 'Venda', 55.00, '2023-09-17 15:30:00', 1, 007),
                  (8, 'Compra', -90.00, '2023-09-17 16:15:00', NULL, NULL)
            '''
      )

      conn = None
      try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            for command in commands:
                  cur.execute(command)
                  
            cur.close()
            conn.commit()
      except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            
      finally:
            if conn is not None:
                  conn.close()
                  
def delete_data():
      #Deleta tuplas das relações
      
      commands = (       
            #Elimina o cliente Henrique Brito, cujo ID = 070 e não está sendo usado em outras relações
            '''
            DELETE FROM Clientes WHERE ID_cliente = 070 ;
            ''',
      )
      conn = None
      try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            
            for i, command in enumerate(commands, start=1):
                  cur.execute(command)
                  
                  results = cur.fetchall()
                  
                  for row in results:
                        print(row)
                  
            cur.close()
            conn.commit()
      
      except (Exception, psycopg2.DatabaseError) as error:
            print(error)
      finally:
            if conn is not None:
                  conn.close()
      
def search_data():
      #Cria relações com o restultado das buscas
      
      commands = (
            #Busca os produtos que não estão disponíveis no estoque
            '''
            SELECT Produtos.NomeProduto 
            FROM Produtos LEFT JOIN Estoque ON Produtos.ID_produto = Estoque.ID_produto
            WHERE Estoque.QuantidadeEmEstoque <= 0 OR Estoque.QuantidadeEmEstoque IS NULL;
            ''',
            
            #Busca os funcionários com pelo menos 1 dependente
            '''
            SELECT pNome, uNome, n_dependentes
            FROM Funcionarios
            WHERE n_dependentes > 0;
            ''',
            
            #Busca todas as avaliações feitas por um cliente específico.
            '''
            SELECT AvaliacoesComentarios.Classificacao, AvaliacoesComentarios.Comentario, AvaliacoesComentarios.DataAvaliacao
            FROM AvaliacoesComentarios
            WHERE AvaliacoesComentarios.ID_cliente = 157;
            ''',
            
            #Busca todas as transações feitas por clientes
            '''
            SELECT Transacoes_Financeiras.ID_transacao, Transacoes_Financeiras.TipoTransacao, Transacoes_Financeiras.Valor, Clientes.pNome, Clientes.uNome
            FROM Transacoes_Financeiras LEFT JOIN Clientes ON Transacoes_Financeiras.ID_cliente = Clientes.ID_cliente;
            ''',
            
            #Busca todos os pedidos com os nomes dos respectivos clientes
            '''
            SELECT Pedidos.ID_pedido, Pedidos.DataHoraPedido, Clientes.pNome, Clientes.uNome
            FROM Pedidos INNER JOIN Clientes ON Pedidos.ID_cliente = Clientes.ID_cliente;
            ''',
            
            #Busca todos os produtos em estoque com o nome de seu fornecedor
            '''
            SELECT Produtos.NomeProduto, Estoque.QuantidadeEmEstoque, Fornecedores.NomeFornecedor
            FROM Produtos INNER JOIN Estoque ON Produtos.ID_produto = Estoque.ID_produto 
            INNER JOIN Fornecedores ON Estoque.ID_fornecedor = Fornecedores.ID_fornecedor;
            ''',
            
            #Busca todos os itens de pedido para um pedido específico com informações sobre o produto
            '''
            SELECT Itens_Pedido.ID_item, Produtos.NomeProduto, Itens_Pedido.Quantidade, Itens_Pedido.PrecoUnitario
            FROM Itens_Pedido INNER JOIN Produtos ON Itens_Pedido.ID_produto = Produtos.ID_produto
            WHERE Itens_Pedido.ID_pedido = 1;
            ''',
            
            #Busca todos os pedidos feitos por uma mesa específica com informações sobre o pedido
            '''
            SELECT Pedidos.ID_pedido, Pedidos.DataHoraPedido, Pedidos.StatusPedido, Mesa_Atendimento.NumeroMesa
            FROM Pedidos INNER JOIN Mesa_Atendimento ON Pedidos.ID_mesa = Mesa_Atendimento.ID_mesa
            WHERE Pedidos.ID_cliente = 411;
            '''
      )
      
      conn = None
      try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            
            for i, command in enumerate(commands, start=1):
                  cur.execute(command)
                  
                  results = cur.fetchall()
                  
                  print(f"Resultados da consulta {i}:")
                  for row in results:
                        print(row)
                  
                  print("-" * 30)
                  
            cur.close()
            conn.commit()
      
      except (Exception, psycopg2.DatabaseError) as error:
            print(error)
      finally:
            if conn is not None:
                  conn.close()
                  
def update_data():
      
      commands = (      
            #Aumento para o funcionário 2 (Lucas)
            '''
            UPDATE Funcionarios
            SET Salario = 2150.00
            WHERE ID_funcionario = 2 ;
            ''',
            
            #Aumento de 5% para todos os funcionários
            '''
            UPDATE Funcionarios
            SET Salario = Salario * 1.05;
            '''
      )
      
      conn = None
      try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            for command in commands:
                  cur.execute(command)
            cur.close()
            conn.commit()
            
      except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            
      finally:
            if conn is not None:
                  conn.close()

if __name__ == "__main__":
      create_tables()
      insert_data()
      search_data()
      delete_data()
      update_data()