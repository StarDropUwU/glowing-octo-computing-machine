from datetime import datetime
from sqlalchemy import Sequence, create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from config import Config

db = create_engine(Config.SQLALCHEMY_DATABASE_URI,echo=True)

Base = declarative_base()
Session = sessionmaker(bind=db)

class FinancialOperation(Base):
    __tablename__ = "financialOperations"
    id = Column(Integer, Sequence("fo_id_seq"), primary_key=True)
    tipo_operacao = Column(String(50), nullable=False)
    valor = Column(Float, nullable=False)
    data = Column(DateTime, default=datetime.now())
    descricao = Column(String(200))
    """Modelo de dados usado para registro das operações financeiras."""

    def create_exportable(self):
        return {
            'id': self.id,
            'tipo_operacao': self.tipo_operacao,
            'valor': self.valor,
            'data': self.data,
            'descricao': self.descricao
        }
    """Método para converter o objeto da operação financeira em um dicionário à ser retornado no fim das operações."""
    
class TransactionHistory(Base):
    __tablename__ = "transactionHistory"
    id = Column(Integer, Sequence("th_id_seq"), primary_key=True)
    operation_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    mudancas = Column(String(200))
    """Modelo de dados usado para registro do histórico de mudanças das operações financeiras."""

Base.metadata.create_all(db)

session = Session()


