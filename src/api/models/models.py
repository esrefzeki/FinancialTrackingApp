from src.api.infrastructure.persistance.db_manager import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True, unique=True)
    gender = Column(Integer, nullable=False)
    birthday = Column(Date)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    current_balance = Column(Float, default=0, nullable=False)

    expense = relationship("Expense", back_populates="user")
    expense_type = relationship("ExpenseTypes", back_populates="user")
    income = relationship("Income", back_populates="user")
    income_type = relationship("IncomeTypes", back_populates="user")
    # expense_instalment = relationship("ExpenseInstalment", back_populates="user")


class ExpenseTypes(Base):
    __tablename__ = "expensetypes"

    id = Column(Integer, primary_key=True, nullable=False)
    type_expense = Column(Integer, nullable=False, unique=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="expense_type")
    expense_relation = relationship("Expense", back_populates="expense_type_relation")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, nullable=False)
    expense_name = Column(String, default="New Expense", index=True)
    expense_type_id = Column(Integer, ForeignKey("expensetypes.id", ondelete="CASCADE"), nullable=False, index=True)
    amount = Column(Float)
    status = Column(Boolean, default=False, nullable=False)
    instalment = Column(Integer, default=0)
    payment_date = Column(Date)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="expense")
    expense_type_relation = relationship("ExpenseTypes", back_populates="expense_relation")


class IncomeTypes(Base):
    __tablename__ = "incometypes"

    id = Column(Integer, primary_key=True, nullable=False)
    type_income = Column(Integer, nullable=False, unique=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="income_type")
    income_relation = relationship("Income", back_populates="income_type_relation")


class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, nullable=False)
    income_name = Column(String, default="New Income", index=True)
    income_type_id = Column(Integer, ForeignKey("incometypes.id", ondelete="CASCADE"), default=1, nullable=False, index=True)
    amount = Column(Float)
    recurrence = Column(Integer, default=0)
    payment_date = Column(Date)
    status = Column(Boolean, default=True, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="income")
    income_type_relation = relationship("IncomeTypes", back_populates="income_relation")
