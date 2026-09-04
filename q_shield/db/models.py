from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class ScanSession(Base):
    """Tracks historical scan sessions across codebases and target environments."""
    __tablename__ = "scan_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    target_project: Mapped[str] = mapped_column(String(255), nullable=False)
    initiated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(50), default="PENDING") # PENDING, IN_PROGRESS, COMPLETED, FAILED
    
    # Relationships
    risk_metric: Mapped[Optional["RiskSnapshot"]] = relationship(back_populates="scan", uselist=False)
    cbom_assets: Mapped[list["CBOMAsset"]] = relationship(back_populates="scan")


class RiskSnapshot(Base):
    """Stores calculated Mosca Inequality metrics and QVI scores per scan."""
    __tablename__ = "risk_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scan_sessions.id"), nullable=False)
    qvi_score: Mapped[float] = mapped_column(Float, nullable=False)
    urgency: Mapped[str] = mapped_column(String(20), nullable=False) # CRITICAL, MODERATE, SAFE
    mosca_x: Mapped[int] = mapped_column(Integer, nullable=False)
    mosca_y: Mapped[int] = mapped_column(Integer, nullable=False)
    mosca_z: Mapped[int] = mapped_column(Integer, nullable=False)

    scan: Mapped["ScanSession"] = relationship(back_populates="risk_metric")


class CBOMAsset(Base):
    """Stores individual cryptographic components compliant with CycloneDX 1.6."""
    __tablename__ = "cbom_assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scan_sessions.id"), nullable=False)
    asset_name: Mapped[str] = mapped_column(String(255), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(50), nullable=False) # Source Code, eBPF Socket, Process Memory
    discovered_primitive: Mapped[str] = mapped_column(String(100), nullable=False)
    pqc_target_standard: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    source_location: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    raw_metadata: Mapped[dict] = mapped_column(JSON, default={})

    scan: Mapped["ScanSession"] = relationship(back_populates="cbom_assets")
