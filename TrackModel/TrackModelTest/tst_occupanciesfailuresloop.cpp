#include <QtTest>

// add necessary includes here

class OccupanciesFailuresLoop : public QObject
{
    Q_OBJECT

public:
    OccupanciesFailuresLoop();
    ~OccupanciesFailuresLoop();

private slots:
    void test_case1();
};

OccupanciesFailuresLoop::OccupanciesFailuresLoop() {}

OccupanciesFailuresLoop::~OccupanciesFailuresLoop() {}

void OccupanciesFailuresLoop::test_case1() {}

QTEST_APPLESS_MAIN(OccupanciesFailuresLoop)

#include "tst_occupanciesfailuresloop.moc"
