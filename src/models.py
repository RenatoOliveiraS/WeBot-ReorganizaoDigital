from typing import List, Optional

from sqlalchemy import CHAR, CheckConstraint, Column, Date, DateTime, Enum, ForeignKeyConstraint, Index, Integer, LargeBinary, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import ENUM, LONGBLOB, LONGTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class WeBotPastasEmpresas(Base):
    __tablename__ = 'WeBotPastasEmpresas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(255))
    cnpj: Mapped[str] = mapped_column(String(20))
    nomepasta: Mapped[str] = mapped_column(String(255))
    gerado: Mapped[str] = mapped_column(String(10))
    razao_social_atualizar: Mapped[str] = mapped_column(CHAR(1), server_default=text("'N'"))

    WeBotPastasEmpresasEstruturas: Mapped[List['WeBotPastasEmpresasEstruturas']] = relationship('WeBotPastasEmpresasEstruturas', back_populates='empresa')


class WeBotPastasPastas(Base):
    __tablename__ = 'WeBotPastasPastas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nomepasta: Mapped[str] = mapped_column(String(255))

    WeBotPastasEstruturas: Mapped[List['WeBotPastasEstruturas']] = relationship('WeBotPastasEstruturas', back_populates='WeBotPastas_pasta')


class WeBotPastasgrupos(Base):
    __tablename__ = 'WeBotPastasgrupos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[Optional[str]] = mapped_column(String(255))

    WeBotPastasPermissoes: Mapped[List['WeBotPastasPermissoes']] = relationship('WeBotPastasPermissoes', back_populates='grupo')


class WeBotPastastiposPermissao(Base):
    __tablename__ = 'WeBotPastastipos_permissao'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[Optional[str]] = mapped_column(String(50))

    WeBotPastasPermissoes: Mapped[List['WeBotPastasPermissoes']] = relationship('WeBotPastasPermissoes', back_populates='permissao')


class WeBotPastasEstruturas(Base):
    __tablename__ = 'WeBotPastasEstruturas'
    __table_args__ = (
        ForeignKeyConstraint(['WeBotPastas_pasta_id'], ['WeBotPastasPastas.id'], name='WeBotPastasEstruturas_ibfk_2'),
        ForeignKeyConstraint(['pai_id'], ['WeBotPastasEstruturas.id'], name='WeBotPastasEstruturas_ibfk_1'),
        Index('WeBotPastas_pasta_id', 'WeBotPastas_pasta_id'),
        Index('pai_id', 'pai_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    WeBotPastas_pasta_id: Mapped[Optional[int]] = mapped_column(Integer)
    auto: Mapped[Optional[str]] = mapped_column(String(10))
    gerado: Mapped[Optional[str]] = mapped_column(String(10))
    pai_id: Mapped[Optional[int]] = mapped_column(Integer)
    replicar_para_empresas: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'0'"))

    WeBotPastas_pasta: Mapped[Optional['WeBotPastasPastas']] = relationship('WeBotPastasPastas', back_populates='WeBotPastasEstruturas')
    pai: Mapped[Optional['WeBotPastasEstruturas']] = relationship('WeBotPastasEstruturas', remote_side=[id], back_populates='pai_reverse')
    pai_reverse: Mapped[List['WeBotPastasEstruturas']] = relationship('WeBotPastasEstruturas', remote_side=[pai_id], back_populates='pai')
    WeBotPastasEmpresasEstruturas: Mapped[List['WeBotPastasEmpresasEstruturas']] = relationship('WeBotPastasEmpresasEstruturas', back_populates='estrutura')
    WeBotPastasPermissoes: Mapped[List['WeBotPastasPermissoes']] = relationship('WeBotPastasPermissoes', back_populates='estrutura')


class WeBotPastasEmpresasEstruturas(Base):
    __tablename__ = 'WeBotPastasEmpresasEstruturas'
    __table_args__ = (
        ForeignKeyConstraint(['empresa_id'], ['WeBotPastasEmpresas.id'], name='WeBotPastasEmpresasEstruturas_ibfk_1'),
        ForeignKeyConstraint(['estrutura_id'], ['WeBotPastasEstruturas.id'], name='WeBotPastasEmpresasEstruturas_ibfk_2'),
        Index('empresa_id', 'empresa_id'),
        Index('estrutura_id', 'estrutura_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[int] = mapped_column(Integer)
    estrutura_id: Mapped[int] = mapped_column(Integer)
    nomepasta: Mapped[str] = mapped_column(String(255))
    caminho_completo: Mapped[str] = mapped_column(String(255))
    nivel: Mapped[int] = mapped_column(Integer)
    gerado: Mapped[str] = mapped_column(CHAR(1), server_default=text("'N'"))
    razao_social_atualizar: Mapped[str] = mapped_column(CHAR(1), server_default=text("'N'"))
    old_path: Mapped[Optional[str]] = mapped_column(Text)

    empresa: Mapped['WeBotPastasEmpresas'] = relationship('WeBotPastasEmpresas', back_populates='WeBotPastasEmpresasEstruturas')
    estrutura: Mapped['WeBotPastasEstruturas'] = relationship('WeBotPastasEstruturas', back_populates='WeBotPastasEmpresasEstruturas')


class WeBotPastasPermissoes(Base):
    __tablename__ = 'WeBotPastasPermissoes'
    __table_args__ = (
        ForeignKeyConstraint(['estrutura_id'], ['WeBotPastasEstruturas.id'], name='WeBotPastasPermissoes_ibfk_1'),
        ForeignKeyConstraint(['grupo_id'], ['WeBotPastasgrupos.id'], name='fk_grupo_id'),
        ForeignKeyConstraint(['permissao_id'], ['WeBotPastastipos_permissao.id'], name='fk_permissao_id'),
        Index('estrutura_id', 'estrutura_id'),
        Index('fk_grupo_id', 'grupo_id'),
        Index('fk_permissao_id', 'permissao_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    estrutura_id: Mapped[Optional[int]] = mapped_column(Integer)
    grupo_id: Mapped[Optional[int]] = mapped_column(Integer)
    permissao_id: Mapped[Optional[int]] = mapped_column(Integer)

    estrutura: Mapped[Optional['WeBotPastasEstruturas']] = relationship('WeBotPastasEstruturas', back_populates='WeBotPastasPermissoes')
    grupo: Mapped[Optional['WeBotPastasgrupos']] = relationship('WeBotPastasgrupos', back_populates='WeBotPastasPermissoes')
    permissao: Mapped[Optional['WeBotPastastiposPermissao']] = relationship('WeBotPastastiposPermissao', back_populates='WeBotPastasPermissoes')


t_agendamento_empresas = Table(
    'agendamento_empresas', Base.metadata,
    Column('agendamento_id', Integer, nullable=False),
    Column('pessoa_id', Integer),
    ForeignKeyConstraint(['agendamento_id'], ['agendamentos.id'], name='agendamento_empresas_ibfk_1'),
    ForeignKeyConstraint(['pessoa_id'], ['pessoas.id'], name='agendamento_empresas_ibfk_2'),
    Index('agendamento_id', 'agendamento_id'),
    Index('pessoa_id', 'pessoa_id')
)


t_agendamento_processos = Table(
    'agendamento_processos', Base.metadata,
    Column('agendamento_id', Integer, primary_key=True, nullable=False),
    Column('servico_id', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['agendamento_id'], ['agendamentos.id'], name='agendamento_processos_ibfk_1'),
    ForeignKeyConstraint(['servico_id'], ['processos_disponiveis.id'], name='agendamento_processos_ibfk_2'),
    Index('servico_id', 'servico_id')
)
