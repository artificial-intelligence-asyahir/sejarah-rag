from openai import AsyncOpenAI
from ragas.embeddings.base import embedding_factory, HuggingfaceEmbeddings, LangchainEmbeddingsWrapper
from ragas.llms import llm_factory
from ragas.metrics.collections import AnswerRelevancy
from ragas.metrics.collections import Faithfulness, ContextPrecision, ContextRecall

from app.service.llm_query_service import answer

client = AsyncOpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
)

llm = llm_factory("gemma4", provider="openai", client=client, max_tokens=8192, )

def faithfulness_score(question: str, response: str, contexts: list[str]):
    scorer = Faithfulness(llm=llm)
    result = scorer.score(
        user_input=question,
        response=response,
        retrieved_contexts=contexts
    )
    return result.value

def context_precision_score(question: str, ground_truth: str, contexts: list[str]):
    scorer = ContextPrecision(llm=llm)
    result = scorer.score(
        user_input=question,
        reference=ground_truth,
        retrieved_contexts=contexts
    )
    return result.value

def context_recall_score(question: str, ground_truth: str, contexts: list[str]):
    scorer = ContextRecall(llm=llm)
    result = scorer.score(
        user_input=question,
        retrieved_contexts=contexts,
        reference = ground_truth
    )

    return result.value

def answer_relevancy_score(question: str, response: str):
    embeddings = embedding_factory("huggingface", "sentence-transformers/all-MiniLM-L6-v2")
    scorer = AnswerRelevancy(llm=llm, embeddings=embeddings)
    result = scorer.score(
        user_input=question,
        response=response
    )

    return result.value

async def discrete_metric():
    pass


if __name__ == "__main__":
    import asyncio

    sample = {
        "question": "Jelaskan latar belakang kehadiran James Brooke di Sarawak.",
        "ground_truth": """
            - Pada peringkat awal, menjalankan aktiviti pengembaraan di antara Sarawak dan Singapura dengan Kapalnya Royalist.
- Mendapat sokongan pihak British melalui angkatan tentera laut.
- Menerima pelawaan Pengiran Raja Muda Hashim untuk menyelesaikan masalah di Sarawak.
- Mengenakan syarat, iaitu Pengiran Raja Muda Hashim perlu menyerahkan Sarawak kepada beliau.
- Membantu menyelesaikan masalah pemberontakan Dayak yang sedang berlaku
- Sebagai ganjaran James Brooke telah diberikan gelaran Raja Sarawak oleh Raja Muda Hashim.  telah disahkan dan diperkenankan oleh Sultan Brunei.
            """,
        "response": """
        Latar belakang kehadiran James Brooke di Sarawak dicirikan oleh keadaan politik yang tidak stabil serta konflik dalaman masyarakat tempatan pada masa itu, yang membolehkan beliau memanfaatkan situasi tersebut untuk memperluaskan kuasa.

Berikut adalah perincian latar belakangnya:

1.  **Kekosongan dan Konflik Politik:** Sebelum dominasi Brooke, Sarawak berada di bawah pengaruh Kesultanan Brunei, namun Kawasan ini turut mempunyai ketegangan politik antara pelbagai kumpulan etnik (seperti Melayu, Iban, dan Cina). Perpecahan dan pertelingkahan dalam kalangan masyarakat tempatan inilah yang menjadi peluang utama bagi James Brooke.
2.  **Peranan Sebagai Pengantara:** Pada peringkat awal, Brooke terlibat sebagai seorang pengantara konflik di Sarawak. Ini membolehkannya mengenal pasti kelemahan kuasa sedia ada dan membina pengaruh serta kredibiliti diri.
3.  **Strategi Pengembangan Kuasa:** Untuk merealisasikan cita-citanya, James Brooke menggunakan pelbagai strategi yang sistematik, iaitu:
    *   **Rundingan (Diplomasi):** Menggunakan perbincangan rasmi untuk mendapatkan hak dan kuasa daripada pihak berkuasa tempatan (seperti Sultan Brunei).
    *   **Ugutan/Ancaman:** Bersedia untuk menggunakan ancaman atau paksaan apabila rundingan gagal, menunjukkan kekuatan pengaruhnya.
    *   **Sokongan Kuasa Asing:** Beliau memperoleh sokongan penting daripada tentera laut British, yang memberikan kedudukan dan ketenteraan yang kukuh dalam usaha pengukuhan kuasanya di Sarawak.

Secara ringkas, James Brooke memanfaatkan kelemahan politik dan konflik sosial yang sedia ada di Sarawak untuk menguasai pentadbiran dan ekonomi kawasan tersebut, lantas mewujudkan Dinasti Brooke sebagai Raja Putih Sarawak yang pertama.
        """,
        "contexts": [
            "James Brooke, Raja Putih Sarawak yang pertama \n\nCharles Brooke, Raja Putih Sarawak yang kedua \n\n \nMukah Oya Tanjung Sibu Datu Kanowit Sarikei Rajang Kapit ak r Kuching Bau Sri Batang Bahagian BahagianPertama AmanLupar Kedua S. Kawasan jajahan keluarga Brooke di Sarawak. ## **Cerna Minda** \n\nNamakan kawasan yang berjaya dikuasai oleh James Brooke. ## **KPS** \n\nBincangkan kaedah yang digunakan oleh Charles Brooke dalam usaha memperluas kuasa Dinasti Brooke di Sarawak.",
            "**116** A \n\n## **Pengukuhan Kuasa James Brooke** \n\nSetelah memperoleh kuasa di Sarawak, James Brooke berusaha mengukuhkan kuasanya. Jadual: Usaha dan Tindakan James Brooke Mengukuhkan Kuasa \n\n|||e|James Brooke memperoleh bantuan dan sokongan daripada|\n|---|---|---|---|\n|**Kekuatan Tentera**||¢|tentera laut British.",
            "Seterusnya, James Brooke dan keluarganya berusaha meluaskan kuasa mereka ke seluruh Sarawak. ## **Sarawak Ketika Kehadiran James Brooke** \n\nkawasan ekonomi yang penting. Mahkota ke kawasan ini sebagai pembesar Brunei untuk menguasai ekonomi. e Sultan Brunei menghantar Pengiran Indera \n\nMelayu bertumpu di Lidah Tanah yang terletak di sekitar Sungai Sarawak. Kawasan ini menjadi pusat perdagangan dan pentadbiran.",
            "¢ Sempadan Sarawak itu masih \n\nCharles Vyner Brooke, Raja Putih Sarawak yang \n\nJelaslah bahawa kelicikan dan kemampuan James Brooke menggunakan pelbagai strategi membolehkannya berjaya mendapatkan Sarawak daripada Sultan Brunei. Perpecahan dan konflik masyarakat tempatan memudahkan usaha James Brooke ini. Dalam hal ini, sejarah membuktikan bahawa tanpa sifat bersatu padu dan berwaspada, orang OS i ketiga(1917-1946).",
            "James Brooke menggunakan empat strategi dalam usaha mencapai matlamatnya. ## **1. Rundingan** \n\nHashim apabila diminta untuk menyelesaikan pertelingkahan yang berlaku di Sarawak. Brooke dan tawaran ini dilakukan sebanyak dua kali sebelum James Brooke menerimanya. ## **2. Ugutan** \n\nMuda Hashim yang cuba berdolak-dalik dan tidak bersetuju dengan rundingan yang dilakukan sebelumnya, iaitu menyerahkan Sarawak kepadanya.",
            "Melayu, Iban dan Sarawak Cina. Charles Brooke Orang Melayu dalam mewujudkan pentadbiran, orang Cina jawatan tertinggi dalam ekonomi dan orang masyarakat Iban, iaitu Iban dalam keselamatan Temenggung. dan ketenteraan. Bandingkan dasar yang (b) dilakukan oleh pihak British Pentadbir dikenali di Negeri-negeri Melayu sebagai Penolong dengan tindakan Dinasti Pegawai Daerah. Brooke di Sarawak dalam Pentadbiran mengamalkan dasar pecah dan perintah berasaskan kaum. berasaskan peribumi di Sabah."
        ]
    }

    result = context_precision_score(sample['question'], sample['ground_truth'], sample['contexts'])
    print(f"Context Precision Score: {result}")

    print("question length: ", len(sample['question']))
    print("ground truth length: ", len(sample['ground_truth']))

    total_context_chars = sum(len(c) for c in sample["contexts"])
    print("context length: ", total_context_chars)
    print("response length: ", len(sample['response']))

    # response, context, references = answer(sample['question'])
    # sample["contexts"] = context
    # sample["response"] = response
    # sample["references"] = references

    # result_relevancy = response_relevancy_score(sample)
    # print(f"Relevancy Score: {result_relevancy}")
    #
    # result_recall = context_recall_score(sample)
    # print(f"Context Recall Score: {result_recall}")
    #
    # result_precision = context_precision_score(sample)
    # print(f"Context Precision Score: {result_precision}")
    #
    # result_faithfulness = faithfulness_score(sample)
    # print(f"Faithfulness Score: {result_faithfulness}")