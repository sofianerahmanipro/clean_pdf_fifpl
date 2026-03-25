import re
import sys
from pathlib import Path
import pikepdf


TAG_REGEX = re.compile(r"\{.*?\}")
FONT_ZERO_REGEX = re.compile(r'(/\w+)\s+0\s+Tf')


def field_contains_tag(field):
    if "/V" in field and TAG_REGEX.search(str(field["/V"])):
        return True
    if "/T" in field and TAG_REGEX.search(str(field["/T"])):
        return True
    return False


def fix_field(field, default_size, dry_run):
    fixed = 0
    has_tag = field_contains_tag(field)

    if has_tag:
        print(f"[TAG] {field.get('/T', '')}")

        # Corrige DA
        if "/DA" in field:
            da = str(field["/DA"])
            new_da = FONT_ZERO_REGEX.sub(rf'\1 {default_size} Tf', da)

            if da != new_da:
                print("  → DA corrigé")
                if not dry_run:
                    field["/DA"] = pikepdf.String(new_da)
                fixed += 1

        # Supprime AP
        if "/AP" in field:
            print("  → AP supprimé")
            if not dry_run:
                del field["/AP"]

    # Widgets
    if "/Kids" in field:
        for kid in field["/Kids"]:
            if has_tag:
                if "/AP" in kid:
                    print("  → AP widget supprimé")
                    if not dry_run:
                        del kid["/AP"]

                if "/DA" in kid:
                    da = str(kid["/DA"])
                    new_da = FONT_ZERO_REGEX.sub(rf'\1 {default_size} Tf', da)
                    if da != new_da:
                        print("  → DA widget corrigé")
                        if not dry_run:
                            kid["/DA"] = pikepdf.String(new_da)

            fixed += fix_field(kid, default_size, dry_run)

    return fixed


def main():
    input_path = Path(sys.argv[1])
    output_path = input_path.with_stem(input_path.stem + "_fixed")

    with pikepdf.open(input_path) as pdf:

        if "/AcroForm" in pdf.Root:
            acroform = pdf.Root["/AcroForm"]
            acroform["/NeedAppearances"] = True

            total = 0
            for field in acroform.get("/Fields", []):
                total += fix_field(field, 10, False)

        pdf.save(output_path)

    print(f"\n✅ Corrigé → {output_path}")


if __name__ == "__main__":
    main()