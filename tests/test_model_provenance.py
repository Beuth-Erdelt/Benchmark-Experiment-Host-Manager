"""
Model provenance: which weights answered a phase of the agent.

The vLLM manifests in ``agent/k8s/`` serve a model as
``<Hugging Face repository>@<commit prefix>``; any other served name is pinned
by nobody but its provider. Reports and trajectory record which of the two it was.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import re
import unittest
from pathlib import Path

from agent.harness.model_client import model_provenance, provenance_line

_MANIFESTS = sorted((Path(__file__).resolve().parent.parent / "agent" / "k8s").glob("vllm-*.yml"))


class ModelProvenanceTest(unittest.TestCase):
    def test_self_hosted_model_with_pinned_weights(self):
        provenance = model_provenance("Qwen/Qwen3.8-27B-FP8@1a2b3c4d5e6f", "http://localhost:8001/v1")
        self.assertEqual(provenance, {
            "model": "Qwen/Qwen3.8-27B-FP8", "pinned": True,
            "weights_source": "https://huggingface.co/Qwen/Qwen3.8-27B-FP8",
            "weights_revision": "1a2b3c4d5e6f", "endpoint": None,
        })
        self.assertEqual(provenance_line(provenance),
                         "Model: Qwen/Qwen3.8-27B-FP8, weights revision 1a2b3c4d5e6f "
                         "from https://huggingface.co/Qwen/Qwen3.8-27B-FP8.")

    def test_hosted_api_names_the_provider(self):
        provenance = model_provenance("google/gemma-4-31b-it", "https://openrouter.ai/api/v1")
        self.assertFalse(provenance["pinned"])
        self.assertEqual(provenance["endpoint"], "openrouter.ai")
        self.assertEqual(provenance_line(provenance),
                         "Model: google/gemma-4-31b-it via openrouter.ai. The weights are not "
                         "pinned: the provider may serve other weights under this name.")

    def test_local_and_private_endpoints_are_not_named(self):
        for base_url in ("http://localhost:8001/v1", "http://127.0.0.1:8000/v1",
                         "http://10.0.0.5:8000/v1", "http://bexhoma-agent-model:8000/v1",
                         "http://bexhoma-agent-model.ns.svc:8000/v1", "not a url"):
            with self.subTest(base_url=base_url):
                self.assertIsNone(model_provenance("some-model", base_url)["endpoint"])
                self.assertNotIn(" via ", provenance_line(model_provenance("some-model", base_url)))

    def test_a_name_without_revision_is_not_pinned(self):
        for name in ("Qwen/Qwen3.8-27B-FP8", "qwen3.5:9b", "repo@main", "a/b@xyz1234"):
            with self.subTest(name=name):
                self.assertFalse(model_provenance(name, "http://localhost:8001/v1")["pinned"])

    def test_every_vllm_manifest_serves_its_repository_with_the_revision(self):
        self.assertTrue(_MANIFESTS)
        for manifest in _MANIFESTS:
            with self.subTest(manifest=manifest.name):
                text = manifest.read_text(encoding="utf-8")
                repository = re.search(r'MODEL_REPO="([^"]+)"', text).group(1)
                self.assertIn('SERVED_MODEL_NAME="${MODEL_REPO}@$(cut -c1-12 "$REVISION_FILE")"', text)
                provenance = model_provenance(f"{repository}@0123456789ab", "http://localhost:8001/v1")
                self.assertTrue(provenance["pinned"])
                self.assertEqual(provenance["model"], repository)


if __name__ == "__main__":
    unittest.main()
