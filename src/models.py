from datetime import datetime
from sqlalchemy import Sequence, create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from config import Config

# Configura a conexão com o banco de dados
db = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)

# Define a classe base para os modelos declarativos
Base = declarative_base()
Session = sessionmaker(bind=db)

class FinancialOperation(Base):
    """
    Modelo de dados para operações financeiras.

    Este modelo armazena informações sobre operações financeiras, como o tipo de operação, valor,
    data da operação e descrição. Os dados são salvos na tabela 'financialOperations'.
    """
    __tablename__ = "financialOperations"

    id = Column(Integer, Sequence("fo_id_seq"), primary_key=True)
    tipo_operacao = Column(String(50), nullable=False)
    valor = Column(Float, nullable=False)
    data = Column(DateTime, default=datetime.now)  # Define a data atual por padrão
    descricao = Column(String(200), nullable=True)  # Campo opcional para descrição da operação

    def create_exportable(self):
        """
        Converte a instância de FinancialOperation em um dicionário exportável.

        :return: Um dicionário contendo os dados da operação financeira.
        """
        return {
            'id': self.id,
            'tipo_operacao': self.tipo_operacao,
            'valor': self.valor,
            'data': self.data.strftime('%Y-%m-%d %H:%M:%S'),  # Formatação amigável para retorno JSON
            'descricao': self.descricao or ""  # Retorna uma string vazia caso a descrição seja None
        }

class TransactionHistory(Base):
    """
    Modelo de dados para histórico de transações.

    Este modelo armazena o histórico de alterações realizadas nas operações financeiras,
    registrando a operação modificada, a data da alteração e uma descrição das mudanças.
    Os dados são salvos na tabela 'transactionHistory'.
    """
    __tablename__ = "transactionHistory"

    id = Column(Integer, Sequence("th_id_seq"), primary_key=True)
    operation_id = Column(Integer, ForeignKey('financialOperations.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.now)  # Timestamp da modificação
    mudancas = Column(String(200), nullable=True)  # Descrição das mudanças feitas

# Cria as tabelas no banco de dados
Base.metadata.create_all(db)

# Instancia uma sessão para interação com o banco de dados
session = Session()
