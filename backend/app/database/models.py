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
)
from sqlalchemy.orm import relationship
import enum

db = SQLAlchemy()


class IconMixin:
    iconName = Column(String(50))
    colorCode = Column(String(50))


class User(db.Model):
    __tablename__ = "user"

    email = Column(String(255), primary_key=True)
    password = Column(LargeBinary)
    fullName = Column(String(255))
    monthlyBudget = Column(Integer)
    currency = Column(String(255), nullable=True)
    shouldGetScrapped = Column(Boolean, default=True)
    initialSetupDone = Column(Boolean, default=False)    
    lastTransactionsScanDate = Column(DateTime, default=None)

    appUserCredentials = relationship("AppUserCredentials", back_populates="user", uselist=False)


class AppUserCredentials(db.Model):
    __tablename__ = "appUserCredentials"

    userEmail = Column(String(255), ForeignKey("user.email"), primary_key=True)
    username = Column(String(255))
    password = Column(String(255))
    identityDocumentNumber = Column(String(255))

    user = relationship("User", back_populates="appUserCredentials")


class UserCategory(db.Model, IconMixin):
    __tablename__ = "userCategory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    categoryName = Column(String(255), nullable=False)
    owner = Column(String(255), ForeignKey("user.email"), nullable=True)
    monthlyBudget = Column(Integer)
    isPinned = Column(Boolean, default=False)

    parentUser = relationship("User")

    def serialize(self):
        """
        Serialize the UserCategory object to a dictionary.
        """
        data = {
            "id": self.id,
            "categoryName": self.categoryName,
            "owner": self.owner,
            "monthlyBudget": self.monthlyBudget,
            "isPinned": self.isPinned,
        }

        return data


class UserCategorySpending(db.Model):
    __tablename__ = "userCategorySpending"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userEmail = Column(String(255), ForeignKey("user.email"), nullable=True)
    userCategoryId = Column(Integer, ForeignKey("userCategory.id"))
    date = Column(Integer, nullable=False, index=True)  # 202311
    spendingAmount = Column(Integer)


class CategoryMonthlyAveragesHistory(db.Model):
    __tablename__ = "categoryMonthlyAveragesHistory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userCategoryId = Column(Integer, ForeignKey("userCategory.id"))
    date = Column(Date)
    averageAmount = Column(Integer)


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = Column(String, primary_key=True, nullable=False)
    arn = Column(String(255), nullable=False)
    userEmail = Column(String(255), ForeignKey("user.email"))
    categoryId = Column(Integer, ForeignKey("userCategory.id"), nullable=False, default=-1)

    transactionAmount = Column(Float)
    paymentDate = Column(DateTime)
    purchaseDate = Column(DateTime)
    shortCardNumber = Column(String(4))
    merchantData = Column(JSON)
    originalCurrency = Column(String(3))
    originalAmount = Column(Float)
    isRecurring = Column(Boolean, default=False)
    isDeleted = Column(Boolean, default=False)

    user = relationship("User")
    recurring_transaction = relationship("RecurringTransactions", back_populates="transaction", uselist=False)
    category = relationship("UserCategory")

    def serialize(self, include_category_name=True):
        """
        Serialize the Transaction object to a dictionary.
        """
        data = {
            "id": self.id,
            "arn": self.arn,
            "userEmail": self.userEmail,
            "categoryId": self.categoryId,
            "transactionAmount": self.transactionAmount,
            "paymentDate": self.paymentDate.isoformat() if self.paymentDate else None,
            "purchaseDate": self.purchaseDate.isoformat() if self.purchaseDate else None,
            "shortCardNumber": self.shortCardNumber,
            "merchantData": self.merchantData,
            "originalCurrency": self.originalCurrency,
            "originalAmount": self.originalAmount,
            "isRecurring": self.isRecurring,
            "isDeleted": self.isDeleted,
        }

        if include_category_name:
            data["categoryName"] = self.category.categoryName if self.category else None

        return data


class UserParsedCategory(db.Model):
    __tablename__ = "userParsedCategory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chargingBusiness = Column(String(255))
    userEmail = Column(String(255), ForeignKey("user.email"), nullable=True)
    targetCategoryId = Column(Integer, ForeignKey("userCategory.id"))


class RecurringTransactions(db.Model, IconMixin):
    __tablename__ = "recurringTransactions"

    id = Column(Integer, primary_key=True)
    userEmail = Column(String(255), ForeignKey("user.email"))
    transaction = relationship("Transaction", back_populates="recurring_transaction")
    transactionId = Column(String, ForeignKey("transaction.id"), nullable=False)
    transactionName = Column(String(50))

    frequencyValue = Column(Integer)
    frequencyUnit = Column(String(50))  # "days", "weeks", "months"

    startDate = Column(DateTime)
    scannedAt = Column(DateTime)

    def serialize(self, include_transaction_data=True):
        """
        Serialize the RecurringTransaction object to a dictionary.
        """
        data = {
            "id": self.id,
            "transactionId": self.transactionId,
            "transactionName": self.transactionName,
            "frequencyValue": self.frequencyValue,
            "frequencyUnit": self.frequencyUnit,
            "startDate": self.startDate.isoformat() if self.startDate else None,
            "scannedAt": self.scannedAt.isoformat() if self.scannedAt else None,
        }

        if include_transaction_data:
            data["transaction"] = self.transaction.serialize() if self.transaction else None

        return data


class UserWarnings(db.Model):
    __tablename__ = "userWarnings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userEmail = Column(String(255), ForeignKey("user.email"), nullable=False)
    failedLoginCount = Column(Integer, nullable=False, default=0)
