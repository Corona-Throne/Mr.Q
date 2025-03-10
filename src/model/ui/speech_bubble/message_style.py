from PyQt5.QtCore import QPoint, QMargins, Qt
from PyQt5.QtGui import (
    QColor, QTextDocument, QTextOption, 
    QFont, QTextCursor, QTextCharFormat,
)
from PyQt5.QtWidgets import QStyledItemDelegate

from src.model.ui.speech_bubble.config import MessageRole, MessageShadow

BUBBLE_PADDING = QMargins(15, 0, 35, 0)
TEXT_PADDING = QMargins(15, 15, 15, 15)
FONT_SIZE = 16

class MessageDelegate(QStyledItemDelegate):
    """
    Draws each message.
    """

    _font = None

    def paint(self, painter, option, index):
        painter.save()
        # Retrieve the who,message uple from our model.data method.
        who, text, color, last = index.model().data(index, Qt.DisplayRole)

        textrect = option.rect.marginsRemoved(BUBBLE_PADDING + TEXT_PADDING)
        # setup text doc
        toption = QTextOption()
        toption.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        font = QFont()
        font.setPointSize(FONT_SIZE)

        doc = QTextDocument(text)
        doc.setDefaultTextOption(toption)
        doc.setDefaultFont(font)
        doc.setDocumentMargin(0)
        if doc.size().width() > textrect.width():
            doc.setTextWidth(textrect.width())
        # set text color
        cursor = QTextCursor(doc)
        text_color = QColor(color)
        char_format = QTextCharFormat()
        char_format.setForeground(text_color)
        cursor.select(QTextCursor.Document)
        cursor.mergeCharFormat(char_format)
        
        # sets the anchor point for the painter to start painting
        if who == MessageRole.USER:
            # option.rect - text width - TEXT_PADDING on x axis - 15(pad it a bit)
            tran_x = int(option.rect.width() - doc.size().width()) \
                - BUBBLE_PADDING.left() - BUBBLE_PADDING.right()
        else: tran_x = 0
        trans = QPoint(tran_x, 0)
        painter.translate(trans)

        # option.rect contains our item dimensions. We need to pad it a bit
        # to give us space from the edge to draw our shape.
        textrect.setWidth(doc.size().width())
        textrect.setHeight(doc.size().height())
        bubblerect = textrect.marginsAdded(TEXT_PADDING)

        # draw the bubble, changing color + arrow position depending on who
        # sent the message. the bubble is a rounded rect, with a triangle in
        # the edge.
        painter.setPen(Qt.NoPen)
        # draw shadow
        if who == MessageRole.AI:
            shadowrect = bubblerect.marginsAdded(QMargins(-1,0,4,2))
            brush_color = QColor(MessageShadow.AI)
            if last: brush_color = QColor(MessageShadow.AI_FOCUS)
        else:
            shadowrect = bubblerect.marginsAdded(QMargins(4,0,-1,2))
            brush_color = QColor(MessageShadow.USER)
        painter.setBrush(brush_color)
        painter.drawRoundedRect(shadowrect, 30, 30)

        brush_color = QColor("#262626")
        painter.setBrush(brush_color)
        painter.drawRoundedRect(bubblerect, 30, 30)
        
        # draw the triangle bubble-pointer, starting from the top left/right.
        if who == MessageRole.USER:
            p1 = bubblerect.topRight()
            painter.drawPolygon(p1 + QPoint(-15, 0), p1 + QPoint(5, -5), p1 + QPoint(0, 15))
        else:
            p1 = bubblerect.topLeft()
            painter.drawPolygon(p1 - QPoint(-15, 0), p1 + QPoint(-5, -5), p1 + QPoint(0, 15))

        # draw the text
        painter.translate(textrect.topLeft())
        doc.drawContents(painter)
        painter.restore()

    def sizeHint(self, option, index):
        _, text, _, _ = index.model().data(index, Qt.DisplayRole)
        textrect = option.rect.marginsRemoved(BUBBLE_PADDING + TEXT_PADDING)
        

        toption = QTextOption()
        toption.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        font = QFont()
        font.setPointSize(FONT_SIZE)

        doc = QTextDocument(text)
        doc.setDefaultTextOption(toption)
        doc.setDefaultFont(font)
        doc.setDocumentMargin(0)
        if doc.size().width() > textrect.width():
            doc.setTextWidth(textrect.width())

        textrect.setWidth(doc.size().width())
        textrect.setHeight(doc.size().height())
        textrect = textrect.marginsAdded(TEXT_PADDING)
        return textrect.size()