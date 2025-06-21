from pyasn1.type import namedtype, tag, univ


class PubKeyHeader(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType("oid", univ.ObjectIdentifier()),
        namedtype.NamedType("parameters", univ.Null()),
    )


class OpenSSLPubKey(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType("header", PubKeyHeader()),
        # This little hack (the implicit tag) allows us to get a Bit String as Octet String
        namedtype.NamedType(
            "key",
            univ.OctetString().subtype(
                implicitTag=tag.Tag(tagClass=0, tagFormat=0, tagId=3)
            ),
        ),
    )


class AsnPubKey(univ.Sequence):
    """ASN.1 contents of DER encoded public key:

    RSAPublicKey ::= SEQUENCE {
         modulus           INTEGER,  -- n
         publicExponent    INTEGER,  -- e
    """

    componentType = namedtype.NamedTypes(
        namedtype.NamedType("modulus", univ.Integer()),
        namedtype.NamedType("publicExponent", univ.Integer()),
    )
