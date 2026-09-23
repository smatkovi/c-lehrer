#ifndef PLOTTER_H
#define PLOTTER_H

#include <QDeclarativeImageProvider>
#include <QVector>

#include "Runner.h"

// Draws what the learner's program printed.
//
// QtQuick 1.1 has no Canvas -- that came with QtQuick 2 -- so the picture is
// painted with QPainter and handed to QML through an image provider. No
// temporary files, no cache-busting by filename: QML asks for
// "image://plot/<n>" and a new n means a new picture.
//
// The picture is the actual teacher in the numerics chapters: an explicit
// Euler step visibly gains energy, a time step past the stability limit
// visibly explodes. Reading that in a sentence convinces nobody. So the
// axes always follow the data, including when the data is absurd.
class Plotter : public QDeclarativeImageProvider
{
public:
    Plotter();

    void setCurves(const QVector<Curve> &curves);
    int revision() const { return m_revision; }

    QImage requestImage(const QString &id, QSize *size,
                        const QSize &requestedSize) override;

private:
    QVector<Curve> m_curves;
    int m_revision = 0;
};

#endif
