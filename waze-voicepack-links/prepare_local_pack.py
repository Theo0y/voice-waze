
import sys
from pathlib import Path

# Chemins du projet
SCRIPT_DIR = Path(__file__).resolve().parent
MP3_UPLOAD_DIR = SCRIPT_DIR / "mp3_upload"

import os

FFMPEG_DIR = SCRIPT_DIR.parent / "tools" / "ffmpeg" / "ffmpeg-9.1-essentials_build" / "bin"

os.environ["FFMPEG_BINARY"] = str(FFMPEG_DIR / "ffmpeg.exe")
os.environ["FFPROBE_BINARY"] = str(FFMPEG_DIR / "ffprobe.exe")

# Permet à Python de trouver les modules du sous-dossier
sys.path.insert(0, str(MP3_UPLOAD_DIR))

import file_ingestion
import file_compression
from ffmpeg_utils import configure_ffmpeg_for_pydub


def main():
    input_directory = MP3_UPLOAD_DIR / "input_packs"
    output_directory = MP3_UPLOAD_DIR / "compressed_packs"
    valid_filenames_file = MP3_UPLOAD_DIR / "valid_waze_filenames.txt"

    print("\n=== PREPARATION LOCALE DU PACK WAZE ===")
    print("Aucune publication sur les serveurs Waze.")

    if not input_directory.is_dir():
        raise FileNotFoundError(f"Dossier introuvable : {input_directory}")

    if not valid_filenames_file.is_file():
        raise FileNotFoundError(f"Liste introuvable : {valid_filenames_file}")

    if output_directory.exists():
        raise FileExistsError(
            f"Le dossier de sortie existe déjà : {output_directory}\n"
            "Aucun fichier ne sera supprimé."
        )

    configure_ffmpeg_for_pydub()

    print("\n--- ETAPE 1 : VALIDATION ---")
    valid_packs = file_ingestion.ingest_mp3_packs(
        str(input_directory),
        str(valid_filenames_file)
    )

    if not valid_packs:
        print("\nAucun pack valide trouvé. Arrêt.")
        return

    print("\n--- ETAPE 2 : COMPRESSION LOCALE ---")
    file_compression.compress_mp3_packs(valid_packs)

    print("\n=== PREPARATION TERMINEE ===")
    print(f"Résultat local : {output_directory}")
    print("Aucun envoi vers Waze effectué.")


if __name__ == "__main__":
    main()
