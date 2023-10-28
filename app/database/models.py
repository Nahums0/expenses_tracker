from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Float,
    Integer,
    LargeBinary,
    String,
    Boolean,
    Date,
    ForeignKey,
    Enum
)
from sqlalchemy.orm import relationship
import enum

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    email = Column(String(255), primary_key=True)
    password = Column(LargeBinary)
    shouldGetScrapped = Column(Boolean, default=True)
    lastTransactionsScanDate = Column(DateTime, default=None)

    appUserCredentials = relationship(
        "AppUserCredentials", back_populates="user", uselist=False
    )


class AppUserCredentials(db.Model):
    __tablename__ = "appUserCredentials"

    userEmail = Column(String(255), ForeignKey("user.email"), primary_key=True)
    username = Column(String(255))
    password = Column(String(255))
    identityDocumentNumber = Column(String(255))

    user = relationship("User", back_populates="appUserCredentials")


class Category(db.Model):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    categoryName = Column(String(255), nullable=False)
    owner = Column(String(255), ForeignKey("user.email"), nullable=True) 

class UserCategoryData(db.Model):
    __tablename__ = "userCategoryData"

    id = Column(Integer, primary_key=True, autoincrement=True)
    categoryId = Column(Integer, ForeignKey("category.id"), nullable=True)
    userEmail = Column(String(255), ForeignKey("user.email"), nullable=True)
    monthlyBudget = Column(Integer)
    monthlySpending = Column(Integer)
    monthlyAverage = Column(Integer)
    isPinned = Column(Boolean, default=False)

    parentCategory = relationship("Category")
    parentUser = relationship("User")


class CategoryMonthlyAveragesHistory(db.Model):
    __tablename__ = "categoryMonthlyAveragesHistory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    categoryId = Column(Integer, ForeignKey("userCategoryData.id"))
    monthlyAverageDate = Column(Date)
    monthlyAverageAmount = Column(Integer)


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = Column(String, primary_key=True, nullable=False)
    arn = Column(String(255), nullable=False)
    userEmail = Column(String(255), ForeignKey("user.email"))
    categoryId = Column(Integer, ForeignKey("category.id"))

    transactionAmount = Column(Float)
    paymentDate = Column(DateTime)
    purchaseDate = Column(DateTime)
    shortCardNumber = Column(String(4))
    merchantData = Column(JSON)
    originalCurrency = Column(String(3))
    originalAmount = Column(Float)
    isRecurring = Column(Boolean, default=False)


    user = relationship("User")
    recurring_transaction = relationship("RecurringTransactions", back_populates="transaction", uselist=False)


class UserParsedCategory(db.Model):
    __tablename__ = "userParsedCategory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chargingBusiness = Column(String(255))
    userEmail = Column(String(255), ForeignKey("user.email"), nullable=True)
    targetCategoryId = Column(Integer, ForeignKey("category.id"))


class RecurringTransactions(db.Model):
    __tablename__ = "recurringTransactions"

    id = Column(Integer, primary_key=True)
    transaction_id = Column(String, ForeignKey("transaction.id"), nullable=False)
    transaction = relationship("Transaction", back_populates="recurring_transaction")

    frequency_value = Column(Integer)
    frequency_unit = Column(String(50)) # "days", "weeks", "months"

    startDate = Column(DateTime)
    scannedAt = Column(DateTime)


class UserWarnings(db.Model):
    __tablename__ = "userWarnings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userEmail = Column(String(255), ForeignKey("user.email"), nullable=False)
    failedLoginCount = Column(Integer, nullable=False, default=0)
