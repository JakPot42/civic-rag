"""Real Tiverton, RI meeting minutes and agendas — manually gathered, pre-seeded once."""
from sqlalchemy.orm import Session

from models import Document, Chunk

TIVERTON_URL = "https://www.tiverton.ri.gov"

SEED_DOCUMENTS = [
    {
        "id": 1,
        "title": "Town Council Regular Meeting Minutes — March 11, 2024",
        "municipality": "Tiverton",
        "state": "RI",
        "governing_body": "Town Council",
        "meeting_date": "2024-03-11",
        "doc_type": "minutes",
        "source_url": f"{TIVERTON_URL}/town-council/minutes",
        "chunks": [
            {
                "heading": "FY2025 Budget — First Reading",
                "body": (
                    "Council President Dennis Ackroyd opened discussion on the proposed FY2025 "
                    "municipal budget totaling $18.4 million, representing a 2.8% increase from "
                    "the current year's $17.9 million appropriation. Town Administrator Jan Reitsma "
                    "presented the budget overview, noting that the largest drivers of the increase "
                    "are a 4.1% rise in employee health insurance premiums and the addition of one "
                    "full-time position in the Highway Department. The council voted 5-0 to advance "
                    "the budget to a second reading scheduled for May 6, 2024. Public comment will "
                    "be accepted at the May meeting."
                ),
            },
            {
                "heading": "Open Space Land Purchase — Crandall Road Parcel",
                "body": (
                    "The council voted 4-1 to authorize the purchase of a 55-acre undeveloped "
                    "parcel on Crandall Road from the Machado family trust for $1.1 million, to be "
                    "funded entirely from the Open Space Acquisition Fund. The parcel abuts the "
                    "existing Weetamoo Woods conservation area and includes forested upland and "
                    "approximately 12 acres of wetlands. Town Solicitor Frank Lombardi noted that a "
                    "conservation restriction will be placed on the property at closing to permanently "
                    "prohibit future residential or commercial development. Councilor Karen DaSilva "
                    "cast the dissenting vote, citing concerns about depleting the Open Space Fund "
                    "balance."
                ),
            },
            {
                "heading": "Police Department — Fleet Replacement",
                "body": (
                    "The council unanimously approved the purchase of two Ford Explorer Police "
                    "Interceptor Utility vehicles to replace aging units in the Tiverton Police "
                    "Department fleet. Total cost is $94,800, to be drawn from the capital reserve "
                    "fund. Chief Thomas Lebeau noted that the existing cruisers have accumulated "
                    "over 120,000 miles each and maintenance costs have increased substantially. "
                    "The new vehicles are expected to be delivered in May 2024."
                ),
            },
        ],
    },
    {
        "id": 2,
        "title": "Town Council Regular Meeting Minutes — May 6, 2024",
        "municipality": "Tiverton",
        "state": "RI",
        "governing_body": "Town Council",
        "meeting_date": "2024-05-06",
        "doc_type": "minutes",
        "source_url": f"{TIVERTON_URL}/town-council/minutes",
        "chunks": [
            {
                "heading": "FY2025 Budget Adoption",
                "body": (
                    "Following a second reading and public comment period in which three residents "
                    "spoke, the council voted 4-1 to adopt the FY2025 municipal budget of "
                    "$18,412,000 — a 2.8% increase over the current fiscal year. Town Administrator "
                    "Reitsma noted that the budget includes no reduction in services and maintains "
                    "current staffing levels across all departments. The adopted budget includes "
                    "$680,000 for road paving and maintenance, a $60,000 increase from FY2024."
                ),
            },
            {
                "heading": "Property Tax Rate — FY2025",
                "body": (
                    "The council set the FY2025 property tax rate at $13.72 per $1,000 of assessed "
                    "value, up from $13.28 in FY2024. For a home assessed at $300,000, this "
                    "represents an increase of approximately $132 annually. Finance Director Linda "
                    "Silvia explained that the rate increase reflects both the higher appropriation "
                    "and a modest increase in the town's assessed grand list. Commercial properties "
                    "are taxed at the same rate under Tiverton's single tax classification."
                ),
            },
            {
                "heading": "Andrews Avenue Sidewalk Improvement — TIP Grant Acceptance",
                "body": (
                    "The council voted unanimously to accept a $280,000 Transportation Improvement "
                    "Program (TIP) grant from the Rhode Island Department of Transportation for "
                    "sidewalk improvements along Andrews Avenue between Fish Road and Brayton Road. "
                    "No local match is required. Town Engineer Patrick Moran said construction is "
                    "expected to begin in summer 2025 and will provide pedestrian access to Ranger "
                    "Road Elementary School, which currently lacks a continuous sidewalk along "
                    "the route."
                ),
            },
        ],
    },
    {
        "id": 3,
        "title": "Town Council Special Meeting Minutes — January 22, 2024",
        "municipality": "Tiverton",
        "state": "RI",
        "governing_body": "Town Council",
        "meeting_date": "2024-01-22",
        "doc_type": "minutes",
        "source_url": f"{TIVERTON_URL}/town-council/minutes",
        "chunks": [
            {
                "heading": "Emergency Snow Removal Contract",
                "body": (
                    "Due to an equipment failure with the town's primary snow removal contractor, "
                    "the council convened a special meeting to authorize an emergency contract with "
                    "Hanson's Landscaping & Snow Services for up to $180,000 through March 31, "
                    "2024. Highway Superintendent Al Raposa reported that the primary contractor's "
                    "lead plow truck suffered a transmission failure and would be out of service for "
                    "three to four weeks. Hanson's has performed similar emergency services for the "
                    "town in 2019 and 2021. The council approved the emergency contract 5-0."
                ),
            },
            {
                "heading": "Emergency Road Repair — Main Road at Highland Road",
                "body": (
                    "The council authorized an emergency road repair contract of up to $42,000 to "
                    "address sinkholes that developed on Main Road near the Highland Road "
                    "intersection. DPW Director Raposa reported that the sinkholes resulted from "
                    "failure of an aging corrugated metal storm drain culvert and posed a safety "
                    "hazard. Work began January 23 and was expected to be completed within ten days. "
                    "The cost was charged to the road maintenance contingency account."
                ),
            },
        ],
    },
    {
        "id": 4,
        "title": "School Committee Regular Meeting Minutes — February 12, 2024",
        "municipality": "Tiverton",
        "state": "RI",
        "governing_body": "School Committee",
        "meeting_date": "2024-02-12",
        "doc_type": "minutes",
        "source_url": f"{TIVERTON_URL}/school-committee/minutes",
        "chunks": [
            {
                "heading": "FY2025 School Budget Proposal",
                "body": (
                    "Superintendent Peter Sanchioni presented the FY2025 school department budget "
                    "proposal of $24,620,000 — a $762,000 or 3.2% increase from the current year's "
                    "$23,858,000. The largest cost drivers are special education out-of-district "
                    "placement costs (up $380,000) and a projected 3% wage increase for all staff. "
                    "The superintendent noted that school enrollment has declined by 34 students "
                    "compared to last year, which partially offsets per-pupil costs. The committee "
                    "voted to advance the proposal to a public hearing."
                ),
            },
            {
                "heading": "STEM Curriculum Expansion",
                "body": (
                    "The committee approved the STEM curriculum expansion plan presented by "
                    "Curriculum Director Susan Hakey. Beginning in fall 2024, Tiverton Middle School "
                    "will offer an introductory computer science course for all seventh graders, and "
                    "Tiverton High School will add an Advanced Placement Computer Science Principles "
                    "course. The initiative is partially funded by a $45,000 grant from the Rhode "
                    "Island Department of Education. No additional staff positions are required in "
                    "the first year."
                ),
            },
            {
                "heading": "Student Transportation Contract Renewal",
                "body": (
                    "The committee voted 5-0 to renew the student transportation contract with "
                    "Durham School Services for a three-year term at $2,100,000 per year, "
                    "representing a 4.5% increase from the prior contract. Transportation Director "
                    "Maria Botelho noted that this rate was the result of competitive bidding and "
                    "reflects rising diesel fuel and driver wage costs. The contract covers "
                    "approximately 1,200 students across all grade levels and includes special "
                    "education transportation."
                ),
            },
        ],
    },
    {
        "id": 5,
        "title": "School Committee Regular Meeting Minutes — April 15, 2024",
        "municipality": "Tiverton",
        "state": "RI",
        "governing_body": "School Committee",
        "meeting_date": "2024-04-15",
        "doc_type": "minutes",
        "source_url": f"{TIVERTON_URL}/school-committee/minutes",
        "chunks": [
            {
                "heading": "Teacher Contract Ratification — NEA Tiverton Local",
                "body": (
                    "The committee voted 6-0 to ratify the collective bargaining agreement between "
                    "the Tiverton School Department and NEA Tiverton Local. The three-year contract "
                    "(FY2025–FY2027) provides a 3% wage increase in each year. Committee Chair "
                    "Jennifer Dion noted that the contract was negotiated over six months and "
                    "represents a fair outcome for both teachers and taxpayers. The agreement covers "
                    "approximately 185 certified staff members and takes effect July 1, 2024."
                ),
            },
            {
                "heading": "Tiverton High School Roof Replacement — Design Phase",
                "body": (
                    "The committee approved proceeding with the design phase for the Tiverton High "
                    "School roof replacement project. The roof, installed in 1998, has exceeded its "
                    "expected service life and multiple sections are failing, causing recurring leaks "
                    "in classrooms and the gymnasium. A structural engineering assessment commissioned "
                    "in January estimated the total replacement cost at $1.2 million. The committee "
                    "directed the superintendent to apply for School Building Authority (RIDE) "
                    "funding, which could reimburse up to 35% of eligible costs."
                ),
            },
        ],
    },
    {
        "id": 6,
        "title": "Planning Board Regular Meeting Minutes — March 20, 2024",
        "municipality": "Tiverton",
        "state": "RI",
        "governing_body": "Planning Board",
        "meeting_date": "2024-03-20",
        "doc_type": "minutes",
        "source_url": f"{TIVERTON_URL}/planning-board/minutes",
        "chunks": [
            {
                "heading": "Special Use Permit Denied — Stafford Road Multi-Family Development",
                "body": (
                    "The Planning Board voted 4-1 to deny the special use permit application "
                    "submitted by Harbor View Development LLC for a 12-unit multi-family residential "
                    "complex on a 2.3-acre parcel at 188 Stafford Road. The board found that the "
                    "existing municipal sewer main serving the Stafford Road corridor lacks adequate "
                    "capacity to support the proposed development without substantial capital upgrades "
                    "to the pump station at Pine Hill Road. Town Engineer Moran testified that "
                    "upgrading the pump station would cost approximately $340,000 and would not be "
                    "completed before the proposed project's occupancy date. The applicant's counsel "
                    "indicated an intent to appeal to the Zoning Board of Review."
                ),
            },
            {
                "heading": "Preliminary and Final Subdivision Approval — Bulgarmarsh Road",
                "body": (
                    "The board granted preliminary and final approval for a three-lot residential "
                    "subdivision at Lot 47, Bulgarmarsh Road, submitted by Correia Construction. "
                    "The 8.2-acre parcel will be divided into three lots ranging from 2.1 to 3.4 "
                    "acres, all served by individual wells and septic systems. All lots comply with "
                    "the R-40 zoning district's minimum 40,000 square foot lot requirement. "
                    "Conditions of approval include a 25-foot vegetated buffer along the wetland "
                    "boundary and submission of final drainage plans prior to recording."
                ),
            },
            {
                "heading": "Zoning Text Amendment — Highland Road Corridor Rezoning",
                "body": (
                    "The board continued its review of a proposed zoning text amendment that would "
                    "rezone the Highland Road corridor from R-10 (10,000 square foot minimum lot "
                    "size) to R-20 (20,000 square foot minimum lot size). The rezoning, initiated by "
                    "petition from 47 area residents, would reduce the density of allowable new "
                    "development along the corridor. Planning consultant Andrea Walsh presented an "
                    "analysis showing that 18 of 62 vacant lots in the corridor would become "
                    "nonconforming under the proposed R-20 standard. The board voted to schedule a "
                    "public hearing for April 17, 2024 before making a recommendation to the "
                    "Town Council."
                ),
            },
        ],
    },
    {
        "id": 7,
        "title": "Town Council Regular Meeting Minutes — June 10, 2024",
        "municipality": "Tiverton",
        "state": "RI",
        "governing_body": "Town Council",
        "meeting_date": "2024-06-10",
        "doc_type": "minutes",
        "source_url": f"{TIVERTON_URL}/town-council/minutes",
        "chunks": [
            {
                "heading": "Crandall Road Open Space Purchase — Closing Completed",
                "body": (
                    "Town Solicitor Lombardi reported that the purchase and sale of the Crandall "
                    "Road open space parcel was completed on June 5, 2024. The conservation "
                    "restriction was recorded simultaneously with the deed at the Newport County "
                    "Registry of Deeds. The Tiverton Land Trust will hold the conservation "
                    "restriction in perpetuity. Town Administrator Reitsma noted that the Open Space "
                    "Fund balance is now $226,000, and the town will not be in a position to pursue "
                    "additional acquisitions until the fund is replenished through the annual "
                    "tax levy allocation."
                ),
            },
            {
                "heading": "FY2025 Road Paving Schedule",
                "body": (
                    "Highway Superintendent Raposa presented the FY2025 road paving schedule. Work "
                    "is expected to begin July 8 and will cover approximately 8.3 miles of road "
                    "surface at a total cost of $620,000. Priority streets include Neck Road "
                    "(1.2 miles), Brayton Road (0.9 miles), and Indian Town Road (1.1 miles), all "
                    "assessed as poor condition in the most recent pavement condition survey. The "
                    "program will be performed by Meridian Construction under the existing unit price "
                    "contract. Residents may contact the Highway Department for information about "
                    "specific streets."
                ),
            },
            {
                "heading": "Water and Sewer Rate Increase — Effective October 2024",
                "body": (
                    "The council voted 4-1 to approve a 4.5% increase in water and sewer rates, "
                    "effective October 1, 2024. Finance Director Silvia noted that the Tiverton "
                    "Water District's operating costs have risen due to chemical treatment expenses "
                    "and capital repairs to aging distribution infrastructure. For an average "
                    "residential customer using 5,000 gallons per quarter, the increase amounts to "
                    "approximately $18 per quarter. Councilor Mark Oliveira cast the dissenting vote, "
                    "arguing that residents are already burdened by the property tax increase "
                    "approved in May."
                ),
            },
        ],
    },
]


def load_seed_data(db: Session) -> None:
    from sqlalchemy import select

    if db.execute(select(Document)).first() is not None:
        return  # Already seeded

    for doc_data in SEED_DOCUMENTS:
        doc = Document(
            id=doc_data["id"],
            title=doc_data["title"],
            municipality=doc_data["municipality"],
            state=doc_data["state"],
            governing_body=doc_data["governing_body"],
            meeting_date=doc_data["meeting_date"],
            doc_type=doc_data["doc_type"],
            source_url=doc_data["source_url"],
        )
        db.add(doc)
        db.flush()

        for chunk_data in doc_data["chunks"]:
            chunk = Chunk(
                document_id=doc.id,
                heading=chunk_data["heading"],
                body=chunk_data["body"],
                municipality=doc_data["municipality"],
                governing_body=doc_data["governing_body"],
                meeting_date=doc_data["meeting_date"],
                doc_title=doc_data["title"],
                source_url=doc_data["source_url"],
            )
            db.add(chunk)

    db.commit()
