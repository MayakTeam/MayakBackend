from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, ForeignKey, func

from src.database import Base


class RoleModel(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    
    users: Mapped[list["UserModel"]] = relationship(back_populates="role")  # связь с моделью UserModel
    


class StatusModel(Base):
    __tablename__ = "statuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    reports: Mapped[list["ReportModel"]] = relationship(back_populates="status")


class WorkshopModel(Base):
    __tablename__ = "workshops"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    confirmations: Mapped[list["ConfirmationModel"]] = relationship(back_populates="workshop")

    users: Mapped[list["UserModel"]] = relationship(back_populates="default_workshop")


class AttachmentModel(Base):
    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[Optional[int]] = mapped_column(ForeignKey("reports.id"), nullable=True, index=True)        # прикрепление может быть связано или с отчётом
    comment_id: Mapped[Optional[int]] = mapped_column(ForeignKey("comments.id"), nullable=True, index=True)       # или с комментарием
    confirmation_id: Mapped[Optional[int]] = mapped_column(ForeignKey("confirmations.id"), nullable=True, index=True)  # или с подтверждением
    url: Mapped[str] # путь к файлу на сервере
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)  # пользователь, который загрузил файл
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    report: Mapped[Optional["ReportModel"]] = relationship(back_populates="attachments")
    comment: Mapped[Optional["CommentModel"]] = relationship(back_populates="attachments")
    confirmation: Mapped[Optional["ConfirmationModel"]] = relationship(back_populates="attachments")
    
    # Ограничение, чтобы прикрепление было связано только с одним родителем (отчётом, комментарием или подтверждением)
    __table_args__ = (
       CheckConstraint(
            """
            (CASE WHEN report_id IS NOT NULL THEN 1 ELSE 0 END)
          + (CASE WHEN comment_id IS NOT NULL THEN 1 ELSE 0 END)
          + (CASE WHEN confirmation_id IS NOT NULL THEN 1 ELSE 0 END) = 1
            """,
            name="ck_attachment_exactly_one_parent",
        ),
    )


class CommentModel(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"), index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    user: Mapped["UserModel"] = relationship(back_populates="comments")
    report: Mapped["ReportModel"] = relationship(back_populates="comments")
    attachments: Mapped[list["AttachmentModel"]] = relationship(back_populates="comment")
    

class ConfirmationModel(Base):
    __tablename__ = "confirmations"

    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    workshop_id: Mapped[int] = mapped_column(ForeignKey("workshops.id"), index=True)
    text: Mapped[str]
    confirmed_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["UserModel"] = relationship(back_populates="confirmations")
    report: Mapped["ReportModel"] = relationship(back_populates="confirmations")
    workshop: Mapped["WorkshopModel"] = relationship(back_populates="confirmations")


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), index=True)
    default_workshop_id:  Mapped[Optional[int]] = mapped_column(ForeignKey("workshops.id"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    last_login_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    confirmations: Mapped[list["ConfirmationModel"]] = relationship(back_populates="user")
    reports: Mapped[list["ReportModel"]] = relationship(back_populates="author")
    comments: Mapped[list["CommentModel"]] = relationship(back_populates="user")
    role: Mapped["RoleModel"] = relationship(back_populates="users")
    default_workshop: Mapped[Optional["WorkshopModel"]] = relationship(back_populates="users")


class ReportModel(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    last_updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    
    author: Mapped["UserModel"] = relationship(back_populates="reports")
    status: Mapped["StatusModel"] = relationship(back_populates="reports")
    comments: Mapped[list["CommentModel"]] = relationship(back_populates="report")
    confirmations: Mapped[list["ConfirmationModel"]] = relationship(back_populates="report")
    attachments: Mapped[list["AttachmentModel"]] = relationship(back_populates="report")