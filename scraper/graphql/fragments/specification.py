SPECIFICATION_FRAGMENT = """
fragment SpecificationContent on CategorySpecification {
    isRequired

    specification {
        id
        codename
        label
        type
        class

        datasets {
            codename
            label
            __typename
        }

        dependsOn {
            id
            codename
            __typename
        }

        subSpecifications {
            id
            codename
            label
            type
            __typename
        }

        allSubSpecificationCodenames
        __typename
    }

    __typename
}
"""
